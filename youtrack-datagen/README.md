# YouTrack Test Data Generator
Command line utility to generate randomized test dataset for YouTrack

## Requirements
Python 3.6+

## Installation
Install using `setuptools`:
```
$ python setup.py install
```

## Usage

```
usage: ytdatagen [-h] -p PROJECTS_NUM -u USERS_NUM -i ISSUES_NUM [-d]
                    [--jmeter] [--csv-import] [--verbose] [--debug]

Test data generator for YouTrack

optional arguments:
  -h, --help       show this help message and exit
  -p PROJECTS_NUM  number of projects
  -u USERS_NUM     number of users
  -i ISSUES_NUM    number of issues
  -d               generate default volume of data (projects = 10, users =
                   100, issues = 50000)
  --jmeter         Save data to CSV files as JSON strings
  --csv-import     Save data to CSV files according to YouTrack import scripts
                   requirements
  --verbose        Print meta info to stdout
  --debug          Run in debug mode. Generated data will not be saved to
                   files, but printed to stdout

```

## To-do

* Implement CSV file preparation for YouTrack import scripts