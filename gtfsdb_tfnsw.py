import os
import os.path
import requests
import time
import inspect
from optparse import OptionParser
import zipfile
import json
import urllib2
import pytz
import datetime
from dateutil import parser
from dateutil import tz
from pathlib2 import Path

p = OptionParser()

p.add_option('-u', '--url', default=None, dest='url',
             help='URL of gtfs timetable', metavar='URL')

p.add_option('-k', '--apikey', default=False, dest='apiKey',
             help='API Key', metavar='KEY')

p.add_option('-n', '--filename', default=False, dest='filename',
             help='to be included in the file name', metavar='NAME')

opts,args = p.parse_args()
#opts= p.parse_args()

if opts.apiKey == None:
    print 'Warning: no API Key specified, proceeding without API Key'

if opts.url == None:
    print 'Warning: no Url provided'
    exit(1)


# Replace with your own information:
#api_key = 'apikey 69oLfcnx7UxmHTzvn7NiAaYGh8kMHdvTkngf'
#shared_secret = 'a1b2c3d4e5f6b9999988877766655544'

# Url
# timetables_sydneytrains_url = 'https://api.transport.nsw.gov.au/v1/gtfs/schedule/sydneytrains'
# timetables_buses_url = 'https://api.transport.nsw.gov.au/v1/gtfs/schedule/buses/'
# timetables_ferries_url = 'https://api.transport.nsw.gov.au/v1/gtfs/schedule/ferries'
# timetables_lightrail_url = 'https://api.transport.nsw.gov.au/v1/gtfs/schedule/lightrail'
# timetables_nswtrains_url = 'https://api.transport.nsw.gov.au/v1/gtfs/schedule/nswtrains'


# Header for Authentication
api_key = 'apikey' + ' ' + opts.apiKey
headers = {'Authorization':api_key, 'Accept': 'application/x-google-protobuf'}
fname = 'last_modified.json'

#Check if file exists and contains KEY
def checkFileStatus(url):
    PATH = Path('last_modified.json')
    if PATH.is_file():
        print("last_modified.json exists")
        with open(fname, 'r') as json_data:
            try:
                d1 = json.load(json_data)       # read json object from file
                if url in d1:       # If key exists
                    print("Key exists")
                    return 'file exists - key exists'
                else:       # Key does not exist
                    print("Key DOES NOT exists")
                    return 'file exists - no key exists'
            except ValueError as e:
                print "Can't read JSON object"  # Does not exist OR no read permissions
                return 'file exists - no key exists'
    else:
        print("last_modified.json DOES NOT exist")
        return 'no file exists'

# Check if time-table has been modified since last download
def checkLastDate(response_head, url):
    # Get latest modified date from response header
    latest_modified = parser.parse(response_head.headers['Last-Modified']).astimezone(tz=pytz.timezone('Australia/Sydney'))

    # If modified_date.json exists
    if checkFileStatus(url) == 'file exists - key exists':
        with open(fname, 'r') as json_data:
            # Read last_modified text and get the last modified date
            d1 = json.load(json_data)
            last_mod_date = parser.parse(d1[url]).replace(tzinfo=pytz.timezone('Australia/Sydney'))

        # Check if response has been updated
        if latest_modified > last_mod_date:
            # Update last modified date
            d1[url] = latest_modified.strftime("%d-%B-%Y %H:%M:%S")
            with open('last_modified.json', 'w') as json_data:
                # Read last_modified text and get the last modified date
                print("modified_date updated")
                json.dump(d1, json_data)
            return True

        else:
            print("modified_date is not updated")
            return False

    # If modified_date.json DOES NOT exist of exists without key
    elif checkFileStatus(url) == 'file exists - no key exists':
        last_mod_date = latest_modified
        with open(fname, 'r+') as json_data:
            try:
                d1 = json.load(json_data)
            except ValueError as e:
                print "Can't read JSON object"  # Does not exist OR no read permissions
                d1 = {}     # Create empty json

            print("Adding json object (new KEY)")
            d1[url] = latest_modified.strftime("%d-%B-%Y %H:%M:%S")     # Append json
            json_data.seek(0)
            json.dump(d1, json_data)
            json_data.truncate()
        return True

    # File does not exist
    else:
        d1 = {}
        d1[url] = latest_modified.strftime("%d-%B-%Y %H:%M:%S")
        last_mod_date = latest_modified
        try:
            with open(fname,'w+') as json_data:
                print(fname + " created")
                print("Update last modified date")
                json.dump(d1, json_data)
        except IOError as e:
            print "Error writing json object"  # Does not exist OR no read permissions
        return True



def checkStatus(response):
    try:
        status = response.status_code
        return status
    except StandardError:
        return None

def saveZip(response, fileName):
    file_name = time.strftime("%Y%m%d-%H%M%S_") + fileName + ".zip"
    #response = requests.get(url, headers=headers)
    try:
        file = open(file_name, 'w')
        file.write(response.content)
        file.close()

    except ValueError, error:
        print("Error: Couldn't save file")



if __name__ == '__main__':
    try:
        # Request response header to check if there is an update since last request
        response_head = requests.head(opts.url, headers=headers)
        keep_running = checkLastDate(response_head, opts.url)

        if keep_running:
            while keep_running:    # If true
                print("Downloading response......please wait.......")
                response = requests.get(opts.url, headers=headers)

                if checkStatus(response) == 200:
                    print("status check........200 OK")
                    saveZip(response,opts.filename)
                    print("save response as zip file :) Thank you")
                    break

                else:
                    print("status check........" + checkStatus(response))
                    print("Attempt to download again")

        else:
            print("no file is downloaded since nth new is updated")

    except ValueError, error:
        print("Error: Sth went wrong")


