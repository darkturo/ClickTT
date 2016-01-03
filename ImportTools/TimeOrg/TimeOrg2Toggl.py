#!/usr/bin/python

import sqlite3
import argparse
import sys
import csv

# Some Specific constants
EMAIL = 'Email'
CLIENT = 'Client'
PROJECT = 'Project'
DESCRIPTION = 'Description'
START_DATE = 'Start date'
START_TIME = 'Start time'
DURATION= 'Duration'
TAGS = 'Tags'
BILLABLE = 'Billable'

def parseArgs(argv):
    parser = argparse.ArgumentParser(
                description = """Simple script to migrate data from an the
                                 backup with all the time reports tracked by
                                 TimeOrg to a csv format that can be imported
                                 into Toggl.""" )
    parser.add_argument('-f', '--backup-file', action='store', type=str,
                        required=True, dest='backup', 
                        help="File conatining the backup with the TimeOrg data")
    parser.add_argument('-u', '--user-email', action='store', type=str,
                        required=True, dest='email', 
                        help="Email address to which the report should be associated to")
    parser.add_argument('-o', '--csv-file', action='store', type=str,
                        required=False, dest='csvFile', 
                        help="Target file, where the script will store the CSV output. If nothing is specified, by default the program will use the default std output.")
    parser.add_argument('-c', '--client', action='store', type=str,
                        required=False, dest='client', 
                        help="Use the specified client name for the global report.")
    parser.add_argument('-p', '--project', action='store', type=str,
                        required=False, dest='project', 
                        help="Use the specified project name for the global report.")
    parser.add_argument('-t', '--tags', action='store', type=str,
                        required=False, dest='tags', 
                        help="Use the specified tags for all the entries.")
    parser.add_argument('--billable', action='store', type=bool,
                        required=False, default=True, dest='billable', 
                        help="Specify whether the entries are billable or not. By default I asume yes.")

    return parser.parse_args( argv )

def migrateTimeOrgTimesToCSV(user_email, backup_file, csv_file,
                             client, project, tags, isBillable):
    sqliteQueryResult = extractTimesFromBackup( backup_file )

    csv_fh = sys.stdout
    if csv_file:
        csv_fh = open(csv_file, 'wb')

    with csv_fh as fh:
        field_names = [ EMAIL, CLIENT, PROJECT, DESCRIPTION, 
                        START_DATE, START_TIME, DURATION, 
                        TAGS, BILLABLE ]

        billable_yes_no = "Y"
        if not isBillable:
            billable_yes_no = "N"

        togglCSVEmitter = csv.DictWriter(fh, field_names)
        togglCSVEmitter.writeheader()
        for (sdate, stime, duration) in sqliteQueryResult:
            togglCSVEmitter.writerow({ EMAIL: user_email,
                                       CLIENT: client,
                                       PROJECT: project,
                                       START_DATE: sdate,
                                       START_TIME: stime,
                                       DURATION: duration,
                                       TAGS: tags,
                                       BILLABLE: billable_yes_no})

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
    
    migrateTimeOrgTimesToCSV( options.email, options.backup, options.csvFile,
                              options.client, options.project, options.tags, options.billable )
