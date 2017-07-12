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

p.add_option('-m', '--transport_mode', default=False, dest='mode',
             help='to be included in the file name', metavar='NAME')

p.add_option('-d', '--database', default=None, dest='dsn',
             help='Database connection string', metavar='DSN')

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
                    print("Key DOES NOT exist")
                    return 'file exists - no key exists'
            except ValueError as e:
                print "Can't read JSON object"  # Does not exist OR no read permissions
                return 'file exists - no key exists'
    else:
        print("last_modified.json DOES NOT exist")
        return 'no file exists'

# Check if time-table has been modified since last download. Return T/F AND latest modified date
def checkLastDate(response_head, url):
    # Get latest modified date from response header
    latest_modified = parser.parse(response_head.headers['Last-Modified']).astimezone(tz=pytz.timezone('Australia/Sydney'))

    # If modified_date.json exists
    if checkFileStatus(url) == 'file exists - key exists':
        with open(fname, 'r') as json_data:
            # Read last_modified text and get the last modified date
            d1 = json.load(json_data)
            #last_mod_date = parser.parse(d1[url]).replace(tzinfo=pytz.timezone('Australia/Sydney'))
            last_mod_date = parser.parse(d1[url])

        # Check if response has been updated
        if latest_modified > last_mod_date:
            print("Response has been updated. Updating json file...")
            # Update last modified date
            #d1[url] = latest_modified.strftime("%d-%B-%Y %H:%M:%S")
            d1[url] = str(latest_modified)
            with open('last_modified.json', 'w') as json_data:
                # Read last_modified text and get the last modified date
                print("modified_date updated")
                json.dump(d1, json_data)
            return {'keep_running':True, 'date_modified':latest_modified}

        else:
            print("modified_date has not been updated since last download")
            return {'keep_running':False, 'date_modified':latest_modified}

    # If modified_date.json DOES NOT exist of exists without key
    elif checkFileStatus(url) == 'file exists - no key exists':
        last_mod_date = latest_modified
        with open(fname, 'r+') as json_data:
            try:
                d1 = json.load(json_data)
            except ValueError as e:
                print "Can't read JSON object"  # Does not exist OR no read permissions
                d1 = {}     # Create empty json

            print("Adding json object (new KEY) and updating last modified_date....")
            d1[url] = str(latest_modified)     # Append json
            json_data.seek(0)
            json.dump(d1, json_data)
            json_data.truncate()
        return {'keep_running':True, 'date_modified':latest_modified}

    # File does not exist
    else:
        d1 = {}
        d1[url] = str(latest_modified)
        last_mod_date = latest_modified
        try:
            with open(fname,'w+') as json_data:
                print(fname + " created")
                print("Adding json object (new KEY) and Updating last modified_date....")
                json.dump(d1, json_data)
        except IOError as e:
            print "Error writing json object"  # Does not exist OR no read permissions
        return {'keep_running':True, 'date_modified':latest_modified}

#Check and return code status. E.g. 200
def checkStatus(response):
    try:
        status = response.status_code
        return status
    except StandardError:
        return None

#Run gtfsdb script
def toDatabase(zipFile, mod_date):
    # Save to Database
    print("Saving response to database...")
    cmd = 'gtfsdb-tfnsw/bin/gtfsdb-load --database_url=' + opts.dsn + ' --transport_mode=' + opts.mode + ' --modified_date=' + '\"' +mod_date + '\"' + ' ' + zipFile
    # os.system('gtfsdb-load --database_url="postgresql://localhost/gtfs_db_tfnsw" 20170612-162319_buses.zip')
    os.system(cmd)

#Save response zip file AND run toDatabase function
def saveZip(response, fileName, mod_date):
    #Check if a direcgtory exists
    DIR_NAME = 'zip_files'
    if not os.path.exists(DIR_NAME):
        os.makedirs(DIR_NAME)

    zipfile_name = mod_date.strftime("%Y%m%d-%H%M%S_") + fileName + ".zip"
    file_name = os.path.join(DIR_NAME,zipfile_name)
    # response = requests.get(url, headers=headers)

    try:
        print("Saving zip file....")
        file = open(file_name, 'w')
        file.write(response.content)
        file.close()

        #To Database
        toDatabase(file_name,str(mod_date))

    except ValueError, error:
        print("Error: Couldn't save file")



if __name__ == '__main__':
    try:
        # Request response header to check if there is an update since last request
        response_head = requests.head(opts.url, headers=headers)
        checkLastDate_response = checkLastDate(response_head, opts.url)

        keep_running=checkLastDate_response["keep_running"]
        date_modified=checkLastDate_response["date_modified"]
        #date_modified = date_modified.strftime("%d-%B-%Y %H:%M:%S")
        date_modified_str = str(date_modified)

        if keep_running:
            while keep_running:    # If true
                print("Downloading response......please wait.......")
                response = requests.get(opts.url, headers=headers)

                if checkStatus(response) == 200:
                    print("status check........200 OK")
                    saveZip(response,opts.mode, date_modified)
                    print("DONE :) Thank you")
                    break

                else:
                    print("status check........" + checkStatus(response))
                    print("Attempt to download again")

        else:
            print("no file is downloaded since nth new is updated")

    except ValueError, error:
        print("Error: Sth went wrong")


