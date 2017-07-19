import csv
import requests
import argparse
import datetime as dt
import os
import logging


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
    # SET LOGGING
    logging.basicConfig(filename='veracode_dynamic_scan_scheduler.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S%p', level=logging.DEBUG)

    # SET ARGUMENTS
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

        # IGNORE THE FIRST HEADER LINE
        next(app_list_file)

        # PROCESS EACH REMAINING ENTRY IN CSV
        app_list = csv.reader(app_list_file)
        for row in app_list:
            print 'Processing App ID ' + row[0]
            logging.debug('Processing APP ID ' + row[0])

            # CALCULATE START TIME
            logging.debug('Calculating start time...')
            start_time = (dt.datetime(dt.datetime.now().year, dt.datetime.now().month, dt.datetime.now().day,
                                      int(row[2])) + dt.timedelta(days=int(row[1]))).isoformat()
            logging.debug('Start time is ' + start_time)

            # CALCULATE END TIME
            logging.debug('Calculating end time...')
            end_time = (
                dt.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S') + dt.timedelta(days=int(row[3]))).isoformat()
            logging.debug('End time is ' + end_time)

            # CALL RESCAN API
            logging.debug('Making rescan API for ' + row[0] + '...')
            rescan = rescan_api(username, password, row[0])

            if rescan[0] != 200 or '<error>' in rescan[1]:
                logging.info('Rescan API failed for App ID ' + row[0])
                logging.info('Response code: ' + str(rescan[0]))
                logging.info('API Response: ')
                logging.info(rescan[1])
            else:
                logging.info('Rescan API successful for App ID ' + row[0])

            # CALL SUBMIT SCAN API
            logging.debug('Making submit API for ' + row[0] + '...')
            submit = submit_dynamic_api(username, password, row[0], start_time, end_time)

            if submit[0] != 200 or '<error>' in submit[1]:
                logging.info('Submit API failed for App ID ' + row[0])
                logging.info('[*] Response code: ' + str(submit[0]))
                logging.info('[*] API Response: ')
                logging.info(submit[1])
            else:
                logging.info('Submit API call was successful for App ID ' + row[0] + '. Scan scheduled to start ' + start_time + ' and end on ' + end_time)

    # CLOSE APP LIST FILE
    logging.debug('Closing app_list file...')
    app_list_file.close()
    logging.debug('App_list file closed')

    print 'Script finished. See veracode_dynamic_scan_scheduler.log for details'


if __name__ == "__main__":
    main()
