# Veracode Dynamic Scan Weekly Scheduler

## Required Libraries
CSV, requests, argparse, datetime, os

## Description
Script is intended to be be used to set weekly dynamic scans from an input CSV file.

## Parameters
1.  **-c, --credentials**: path to a text file that has the username on the first line and password on the second line.
2.  **-a, --app_list_file_name**: path to CSV for app list and schedule. Details below.

## CSV File Specifications
Input CSV file requires headers:
1. **app_id**: Application ID in Veracode platform (second number in URL when in an application profile)
2. **days_from_now_start**: The number of days from day script is executed to schdeule the scan. For example, if the script is scheduled to run each Sunday, a "1" would set the dyanmic scan to start on that Monday.
3. **hour_start**: sets the hour (0-23) for when to start the scan on the day (e.g., 9 would start at 9AM)
4. **days_to_run**: sets the number of days to allow the scan to run (e.g., 1 would stop the scan 1 day after the start time)
