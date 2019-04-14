import fitbit
import gather_keys_oauth2 as Oauth2
import pandas as pd
import datetime
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np
import csv
import time


songBPM = "60"
music = ""
# specifiedStart = '00:30'
# specifiedEnd = '01:30'

"""

Pull Data from Database

"""

CLIENT_ID = r'22DG6R'
CLIENT_SECRET = r'abcbc7bc62eee36498be6e70557387d0'

# Define the API Request
server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)


now = str(datetime.datetime.now().strftime("%H:%M"))
start = str((datetime.datetime.now() - datetime.timedelta(minutes=30)).strftime("%H:%M"))
print(now)
print(start)

# For Specified Values

if 'specifiedStart' in locals() and 'specifiedEnd' in locals():
    # Send the API Request
    fit_statsHR = auth2_client.intraday_time_series('activities/heart', base_date='today', detail_level='1sec', start_time=specifiedStart, end_time=specifiedEnd)
    print('WE EXIST')
    print(fit_statsHR['activities-heart-intraday'])

    # Save Heart Data as CSV
    time_list = []
    val_list = []
    for i in fit_statsHR['activities-heart-intraday']['dataset']:
        val_list.append(i['value'])
        time_list.append(i['time'])
    heartdf = pd.DataFrame({'Heart Rate': val_list, 'Time': time_list})

    heartdf.to_csv('/Users/GarrettFlynn/Documents/ConquerFear/heart' + \
                   specifiedStart + '.csv', \
                   columns=['Time', 'Heart Rate'], header=True, \
                   index=False)
    # Convert Dates and other CSV Content into Graphable Lists
    values = []
    dates = []
    datevals = []
    startReadable = []
    endReadable = []

    file = open('/Users/GarrettFlynn/Documents/ConquerFear/heart' + \
                start + '.csv')
    csvfile = csv.reader(file)
    count = 0;
    next(csvfile)
    for row in csvfile:
        values.append(row[1])
        dates.append(row[0])

    for i in dates:
        i = float(i[0:2]) + ((float(i[3:5]) * .01) / .6) + ((float(i[6:8]) * .0001) / .6)
        datevals.append(i)

    specStartRead = float(specifiedStart[0:2]) + ((float(specifiedStart[3:5]) * .01) / .6)
    specEndRead = float(specifiedEnd[0:2]) + ((float(specifiedEnd[3:5]) * .01) / .6)

    bpm = songBPM
    plt.figure()
    plt.plot(datevals, values);

    plt.plot([specStartRead, specEndRead], [int(bpm), int(bpm)])
    plt.title('Heart BPM between ' + specifiedStart + ' and ' + specifiedEnd + '.')
    plt.xlabel("Time (in Hours)")
    plt.ylabel("BPM");
    plt.savefig('/Users/GarrettFlynn/Documents/ConquerFear/plot' + \
                bpm + 'test610.png')
    plt.show

# For Real-Time Values

else:
    # Send the API Request
    fit_statsHR = auth2_client.intraday_time_series('activities/heart', base_date='today', detail_level='1sec', start_time=start, end_time=now)
    print(fit_statsHR['activities-heart-intraday'])

    # Save Heart Data as CSV
    time_list = []
    val_list = []
    for i in fit_statsHR['activities-heart-intraday']['dataset']:
        val_list.append(i['value'])
        time_list.append(i['time'])
    heartdf = pd.DataFrame({'Heart Rate':val_list,'Time':time_list})

    heartdf.to_csv('/Users/GarrettFlynn/Documents/ConquerFear/heart'+ \
                     start+'.csv', \
                    columns=['Time','Heart Rate'], header=True, \
                     index = False)
    # Convert Dates and other CSV Content into Graphable Lists
    values = []
    dates = []
    datevals = []
    startReadable = []
    endReadable = []

    file = open('/Users/GarrettFlynn/Documents/ConquerFear/heart' + \
                start + '.csv')
    csvfile = csv.reader(file)
    count = 0;
    next(csvfile)
    for row in csvfile:
        values.append(row[1])
        dates.append(row[0])

    for i in dates:
        i = float(i[0:2]) + ((float(i[3:5]) * .01) / .6) + ((float(i[6:8]) * .0001) / .6)
        datevals.append(i)

    startReadable = float(start[0:2]) + ((float(start[3:5]) * .01) / .6)
    nowReadable = float(now[0:2]) + ((float(now[3:5]) * .01) / .6)

    # Graph Values
    bpm = songBPM
    plt.figure()
    plt.plot(datevals, values);

    plt.plot([startReadable, nowReadable], [int(bpm), int(bpm)])
    plt.title('Heart BPM between ' + start + ' and ' + now + '.')
    plt.xlabel("Time (in Hours)")
    plt.ylabel("BPM");
    plt.savefig('/Users/GarrettFlynn/Documents/ConquerFear/plot' + \
                bpm + 'testresponsive.png')
    plt.show

