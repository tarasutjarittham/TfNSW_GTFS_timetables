# Query GTFS Realtime Timetables from TfNSW

This script is used to download (and append to database) gtfs-formatted real-time timetables from TfNSW. The script will check if there has been updates from last download and download the updated file accordingly.

There are 2 srcipts:

* gtfsdb_tfnsw.py - This script downloads gtfs timetable in zip format and load them into a specified databse
* gtfs_tfnse_ziponly - This scripts only download gtfs timetable in zip format 


## Getting Started
 These instructions will get you a copy of the project up and running on your local machine or a server for developement and testing purposes.
 
### Prerequisites
TfNSW-GTFSDB requires Python 2.7. Below is a list of Python packages required to be installed for this project (these packages are not included as part of Python standard library):

* protobuf
* sqlalchemy
* pytz
* psycopg2
* python-dateutil
* pathlib2
* request


To install the aforementioned python packages, enter the following command in the command prompt:

```
pip install <Package_name>
```

###Installation


1. Clone or download the project here
2. Go to the project directory by enter:
3. cd ```path_to_the_project```
4. Run script (please see the section below for details)

## Usage

### Input List
Following is a list of input required to be input to the script:

* `-u` OR `--url` : Specify public URI for GTFS realtime Timetables 
* `-k` OR `--apikey`: Specify API Key registered with TfNSW
* `-m` OR `--transport-mode`: Specify mode of tranport for the gtfs data e.g. buses, trains
* `-d` OR `--transport-mode`: Specify database url


### Example Use


gtfsdb_tfnsw.py:

```
python gtfsdb_tfnsw.py -u "https://api.transport.nsw.gov.au/v1/gtfs/schedule/buses" --apikey="<Your API Key>" -m 'buses' --database="postgresql://localhost/db1"
```

gtfsdb_tfnsw\_ziponly.py

```
python gtfsdb_tfnsw_ziponly.py -u "https://api.transport.nsw.gov.au/v1/gtfs/schedule/ferries" --apikey="Ae1BjiMglwAIhIZA3ahIsxqMw1aZqEfdicT7" -m 'ferries'
```
   

### Output
1. GTFS Timetables in a zip file
2. last_modified.json - This is created to keep track of the last modified date of the last download GTFS.
3. For gtfsdb_tfnsw, GTFS data is also stored in the specified database.







