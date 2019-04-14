import fitbit
import gather_keys_oauth2 as Oauth2
import pandas as pd
import datetime
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np
import csv
import time
import os
import subprocess
import pyglet


# Set Initial Parameters of Experiment
songBPM = "60"
music = ""


"""

Have User Listen to Music

"""

# Make Music Choice
os.system('clear')
choice = input("What Would You Like to Listen To?\n1. Metallica | 116 BPM\n2. Red Hot Chili Peppers | 85 BPM\n3. Sly and the Family Stone | 102 BPM\n4. Pink Floyd | 116 BPM\n5. 21 Savage | 146 BPM\n6. DO NOT PRESS\nChoice (number): ")

if choice == "1":
    music = "Metallica - Nothing Else Matters.mp3"
    songBPM = "48"

if choice == "2":
    music = "Red Hot Chili Peppers - Under the Bridge.mp3"
    songBPM = "85"

if choice == "3":
    music = "If You Want Me to Stay.mp3"
    songBPM = "102"

if choice == "4":
    music = "Comfortably Numb.mp3"
    songBPM = "116"

if choice == "5":
    music = "21 Savage - A Lot (Official Audio).mp3"
    songBPM = "148"

if choice == "6":
    music = "Moby - Thousand ( 1993 ).mp3"
    songBPM = "0"
print(choice)
print(music)

dir = 'Songs/' + music

print(dir)
# Play Music
song = pyglet.resource.media(dir)
if music == "Moby - Thousand ( 1993 ).mp3":
    song.seek(60)
    player = song.play()
else:
    player = song.play()

# Save Timestamp
start = str(datetime.datetime.now().strftime("%H:%M"))
end = str((datetime.datetime.now() + datetime.timedelta(minutes=1)).strftime("%H:%M"))
time.sleep(1)
player.pause()

# exit()

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


# Send the API Request
fit_statsHR = auth2_client.intraday_time_series('activities/heart', base_date='today', detail_level='1sec', start_time=start, end_time=end)
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

file = open('/Users/GarrettFlynn/Documents/ConquerFear/heart'+ \
                 start+'.csv')
csvfile = csv.reader(file)
count = 0;
next(csvfile)
for row in csvfile:
    values.append(row[1])
    dates.append(row[0])

for i in dates:
    i = float(i[0:2]) + ((float(i[3:5]) * .01)/.6) + ((float(i[6:8]) * .0001)/.6)
    datevals.append(i)

startReadable = float(start[0:2]) + ((float(start[3:5]) * .01)/.6)
endReadable = float(end[0:2]) + ((float(end[3:5]) * .01)/.6)



"""

Graph Values over Sampling Period

"""

bpm = songBPM
plt.figure()
plt.plot(datevals, values);
plt.plot([startReadable, endReadable], [int(bpm), int(bpm)])
plt.title('Heart BPM between '+ start+ ' and '+ end+ '.')

plt.xlabel("Time (in Hours)")
plt.ylabel("BPM");
plt.savefig('/Users/GarrettFlynn/Documents/ConquerFear/plot'+ \
                 bpm+'musictest.png')
plt.show
