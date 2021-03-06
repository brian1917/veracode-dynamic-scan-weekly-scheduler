# Veracode Dynamic Scan Weekly Scheduler

## Required Libraries
CSV, requests, argparse, datetime, os, logging

## Description
Script to set weekly (or less frequent) dynamic scans from an input CSV file. (Note - it's recommended to build CSV in text editor; Excel CSVs might be an issue.)

## Parameters
1.  **-c, --credentials**: path to a text file that has the username on the first line and password on the second line.
2.  **-a, --app_list_file_name**: path to CSV for app list and schedule. Details below.
3. **-v, --verbose**: sets verbose logging for debugging.

## CSV File Specifications
Input CSV file requires headers (first line of CSV is not processed by script):
1. **app_id**: Application ID in Veracode platform (second number in URL when in an application profile)
2. **days_from_now_start**: The number of days from day script is executed to schdeule the scan. For example, if the script is scheduled to run each Sunday, it would run on 7/2/2017. A 1 would set the dynamic scan for that app to start 1 day after that (7/3/2017). On th next Sunday (7/9/2017), the script would run again and set a dynamic scan to run on 7/10/2017 for that app.
3. **hour_start**: sets the hour (0-23) for when to start the scan on the day (e.g., 9 would start at 9AM)
4. **days_to_run**: sets the number of days to allow the scan to run (e.g., 1 would stop the scan 1 day after the start time)

## Logging
The script creates a **veracode_dynamic_scan_scheduler.log** file. Successfully scheduled scans are recorded as well as any errors. Set the *-v* argument for verbose (debug) logging.
