import csv
import requests
import argparse
import datetime as dt
import os


def rescan_api(api_user, api_password, app_id):
    payload = {'app_id': app_id}
    r = requests.get('https://analysiscenter.veracode.com/api/5.0/rescandynamicscan.do', params=payload,
                     auth=(api_user, api_password))
    return r.status_code, r.content


def submit_dynamic_api(api_user, api_password, app_id, start_time, end_time):
    payload = {'app_id': app_id, 'start_time': start_time, 'end_time': end_time}
    r = requests.get('https://analysiscenter.veracode.com/api/5.0/submitdynamicscan.do', params=payload,
                     auth=(api_user, api_password))
    return r.status_code, r.content


def main():
    # SET UP ARGUMENTS
    parser = argparse.ArgumentParser(
        description='This script schedules dynamic scans based on an input CSV file. Must include a header line '
                    '(first line is skipped). Col 1: APP ID. Col 2: Days out to start (e.g., a 2 schedules the scan '
                    'two days from script run time. If script is always run on a Sunday, that scan will start on a '
                    'Tuesday. Col 3: Hour to start. Col 4: Days to run.')
    parser.add_argument('-c', '--credentials', required=True,
                        help='Text file with username on line 1 and password on line 2')
    parser.add_argument('-a', '--app_list_file_name', required=False,
                        help='CSV file with app list. Use --help for instructions on CSV structure.')
    parser.add_argument('-v', '--verbose', required=False, dest='verbose_out', action='store_true',
                        help='Print verbose output')
    args = parser.parse_args()

    # SET USER NAME/PASSWORD VARIABLES
    username = open(args.credentials, 'r').read().splitlines()[0]
    password = open(args.credentials, 'r').read().splitlines()[1]

    # CREATE API LOG TEXT FILE IF IT DOESN'T EXIST
    if os.path.isfile('api_logs.txt') is False:
        file_name = open('api_logs.txt', 'w')
        file_name.close()

    # OPEN APP LIST FILE
    with open(args.app_list_file_name, 'rb') as app_list_file:

        # OPEN API LOGS FILE
        with open('api_logs.txt', 'a') as logfile:
            # IGNORE THE FIRST HEADER LINE
            next(app_list_file)

            # PROCESS EACH REMAINING ENTRY IN CSV
            app_list = csv.reader(app_list_file)
            for row in app_list:
                print 'Processing App ID ' + row[0]

                # CALCULATE START TIME
                if args.verbose_out is True:
                    print '[*] Calculating start time...'
                start_time = (dt.datetime(dt.datetime.now().year, dt.datetime.now().month, dt.datetime.now().day,
                                          int(row[2])) + dt.timedelta(days=int(row[1]))).isoformat()
                if args.verbose_out is True:
                    print '[*] Start time is ' + start_time

                # CALCULATE END TIME
                if args.verbose_out is True:
                    print '[*] Calculating end time...'
                end_time = (
                    dt.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S') + dt.timedelta(days=int(row[3]))).isoformat()
                if args.verbose_out is True:
                    print '[*] End time is ' + end_time

                # CALL API TO START SCAN
                if args.verbose_out is True:
                    print '[*] Making rescan API for ' + row[0] + '...'
                rescan = rescan_api(username, password, row[0])

                if rescan[0] != 200 or '<error>' in rescan[1]:
                    if args.verbose_out is True:
                        print '[*] Error in rescan API for ' + row[0] + '; writing to log file...'
                    logfile.write(dt.datetime.now().isoformat() + ' Rescan API failed for App ID ' + row[0] + '\n')
                    logfile.write('[*] Response code: ' + str(rescan[0]) + '\n')
                    logfile.write('[*] API Response: ' + '\n')
                    logfile.write(rescan[1] + '\n')
                    if args.verbose_out is True:
                        print '[*] Writing error for rescan API to log file complete'
                else:
                    if args.verbose_out is True:
                        print '[*] Rescan API call was successful; writing to log file...'
                    logfile.write(dt.datetime.now().isoformat() + ' Rescan API accepted for App ID ' + row[0] + '\n')
                    if args.verbose_out is True:
                        print '[*] Writing successful rescan API to log file complete'

                # CALL API TO SUBMIT SCAN
                if args.verbose_out is True:
                    print '[*] Making submit API for ' + row[0] + '...'
                submit = submit_dynamic_api(username, password, row[0], start_time, end_time)

                if submit[0] != 200 or '<error>' in submit[1]:
                    if args.verbose_out is True:
                        print '[*] Error in submit API for ' + row[0] + '; writing to log file...'
                    logfile.write(dt.datetime.now().isoformat() + ': Submit API failed for App ID ' + row[0] + '\n')
                    logfile.write('[*] Response code: ' + str(submit[0]) + '\n')
                    logfile.write('[*] API Response: ' + '\n')
                    logfile.write(submit[1] + '\n \n \n')
                    if args.verbose_out is True:
                        print '[*] Writing error for submit API to log file complete'
                else:
                    if args.verbose_out is True:
                        print '[*] Submit API call was successful; writing to log file...'
                    logfile.write(dt.datetime.now().isoformat() + ' Submit API accepted for App ID ' + row[
                        0] + '; scan scheduled to start for ' + start_time + ' and end on ' + end_time + '\n \n \n')
                    if args.verbose_out is True:
                        print '[*] Writing successful submit API to log file complete'

        # CLOSE LOG FILE
        if args.verbose_out is True:
            print '[*] Closing log file...'
        logfile.close()
        if args.verbose_out is True:
            print '[*] Log file closed'

    # CLOSE APP LIST FILE
    if args.verbose_out is True:
        print '[*] Closing app_list file...'
    app_list_file.close()
    if args.verbose_out is True:
        print '[*] App_list file closed'

    print 'Script finished. See api_logs.txt for details'


if __name__ == "__main__":
    main()
