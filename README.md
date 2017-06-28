# Veracode Dynamic Scan Weekly Scheduler

## Description
Script to set weekly dynamic scans from an input CSV file.

## Required Libraries
CSV, requests, argparse, datetime, os

## Parameters
1.  **-c, --credentials**: path to a text file that has the username on the first line and password on the second line.
2.  **-a, --app_list_file_name**: path to CSV for app list and schedule. Details below.

## CSV File Specifications
Input CSV file requires headers (first line of CSV is not processed by script):
1. **app_id**: Application ID in Veracode platform (second number in URL when in an application profile)
2. **days_from_now_start**: The number of days from day script is executed to schdeule the scan. For example, if the script is scheduled to run each Sunday, it would run on 7/2/2017. A 1 would set the dynamic scan to start 1 day after that or 7/3/2017. It would run again on 7/9/2017 and set a dynamic scan to run on 7/10/2017 for that app.
3. **hour_start**: sets the hour (0-23) for when to start the scan on the day (e.g., 9 would start at 9AM)
4. **days_to_run**: sets the number of days to allow the scan to run (e.g., 1 would stop the scan 1 day after the start time)

## Logging
The script creaes a **api_logs.txt** file on the first run. All subsequent runs append to this file. Successfuly schedules are recorded as well as any errors.
