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
    args = parser.parse_args()

    # SET USER NAME/PASSWORD

    username = open(args.credentials, 'r').read().splitlines()[0]
    password = open(args.credentials, 'r').read().splitlines()[1]

    # CREATE API LOG TEXT FILE IF IT DOESN'T EXIST
    if os.path.isfile('api_logs.txt') is False:
        file_name = open('api_logs.txt', 'w')
        file_name.close()

    with open(args.app_list_file_name, 'rb') as app_list_file:

        with open('api_logs.txt', 'a') as logfile:
            # IGNORE THE FIRST HEADER LINE
            next(app_list_file)

            # PROCESS EACH REMAINING ENTRY IN CSV
            app_list = csv.reader(app_list_file)
            for row in app_list:
                print 'Processing App ID ' + row[0]

                # CALCULATE START AND END TIME
                start_time = (dt.datetime(dt.datetime.now().year, dt.datetime.now().month, dt.datetime.now().day,
                                          int(row[2])) + dt.timedelta(days=int(row[1]))).isoformat()
                end_time = (
                    dt.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S') + dt.timedelta(days=int(row[3]))).isoformat()

                # CALL API TO START SCAN
                rescan = rescan_api(username, password, row[0])
                if rescan[0] != 200 or '<error>' in rescan[1]:
                    logfile.write(dt.datetime.now().isoformat() + ' Rescan API failed for App ID ' + row[0] + '\n')
                    logfile.write('[*] Response code: ' + str(rescan[0]) + '\n')
                    logfile.write('[*] API Response: ' + '\n')
                    logfile.write(rescan[1] + '\n')
                else:
                    logfile.write(dt.datetime.now().isoformat() + ' Rescan API accepted for App ID ' + row[0] + '\n')

                # CALL API TO SUBMIT SCAN
                submit = submit_dynamic_api(username, password, row[0], start_time, end_time)
                if submit[0] != 200 or '<error>' in submit[1]:
                    logfile.write(dt.datetime.now().isoformat() + ': Submit API failed for App ID ' + row[0] + '\n')
                    logfile.write('[*] Response code: ' + str(submit[0]) + '\n')
                    logfile.write('[*] API Response: ' + '\n')
                    logfile.write(submit[1] + '\n \n \n')
                else:
                    logfile.write(dt.datetime.now().isoformat() + ' Submit API accepted for App ID ' + row[
                        0] + '; scan scheduled to start for ' + start_time + ' and end on ' + end_time + '\n \n \n')

        # CLOSE LOG FILE
        logfile.close()

    # CLOSE APP LIST FILE
    app_list_file.close()


if __name__ == "__main__":
    main()
