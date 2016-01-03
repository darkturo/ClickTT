#!/usr/bin/python

import sqlite3
import argparse
import sys
import csv

# Some Specific constants
START_DATE = 'Start date'
START_TIME = 'Start time'
DURATION= 'Duration'

def parseArgs(argv):
    parser = argparse.ArgumentParser(
                description = """Simple script to migrate data from an the
                                 backup with all the time reports tracked by
                                 TimeOrg to a csv format that can be imported
                                 into Toggl.""" )
    parser.add_argument('-f', '--backup-file', action='store', type=str,
                        required=True, dest='backup', 
                        help="File conatining the backup with the TimeOrg data")
    parser.add_argument('-o', '--csv-file', action='store', type=str,
                        required=False, dest='csvFile', 
                        help="Target file, where the script will store the CSV output. If nothing is specified, by default the program will use the default std output.")
    return parser.parse_args( argv )

def migrateTimeOrgTimesToCSV(backup_file, csv_file):
    sqliteQueryResult = extractTimesFromBackup( backup_file )

    csv_fh = sys.stdout
    if csv_file:
        csv_fh = open(csv_file, 'wb')

    with csv_fh as fh:
        field_names = [START_DATE, START_TIME, DURATION]
        togglCSVEmitter = csv.DictWriter(fh, field_names)
        togglCSVEmitter.writeheader()
        for (sdate, stime, duration) in sqliteQueryResult:
            togglCSVEmitter.writerow({ START_DATE: sdate,
                                       START_TIME: stime,
                                       DURATION: duration})

def extractTimesFromBackup(backup_file):
    conn = sqlite3.connect( backup_file )
    c = conn.cursor()

    # This query will extract from the LoginTime and LogoutTime (which
    # represents when you start and stop tracking time with TimeOrg), and then
    # it output a three colum result table, the first colum with contain the 
    # start date, the second column the start time, and the third one wil 
    # contain the duration using the follogin format HH:MM:SS.
    query = """select strftime("%Y-%m-%d", LoginTime), 
                      strftime("%H:%M:%S", LoginTime), 
                      time(strftime('%s', LogoutTime) - strftime('%s', LoginTime),
                           'unixepoch') 
               from times;"""

    # executing the query and returning the array of tuples
    return c.execute( query ).fetchall()

if __name__ == "__main__":
    options = parseArgs(sys.argv[1:])
    
    migrateTimeOrgTimesToCSV( options.backup, options.csvFile )
