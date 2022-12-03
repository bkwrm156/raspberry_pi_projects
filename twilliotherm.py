###This was my first raspberry pi IOT project. A single wire thermometer connected to PI Zero that makes Twilio calls to my cell phone if the freezer gets too warm

import glob
import time
import os
import glob
from twilio.rest import Client
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'XXXXX'
auth_token = 'XXXXX'
client = Client(account_sid, auth_token)

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        global tempc
        tempc = float(temp_string) / 1000.0
        global tempf
        tempf = tempc * 9.0 / 5.0 + 32.0
        return tempc, tempf

while True:
    print(read_temp())
    time.sleep(60)
    if tempf>10:
        message = client.messages.create(
            body="Hey there, I am your freezer. Check me, im warm.PS Charlie is cool.",
            from_='+12565968477',
            to='+13309311044')
        print(message.sid)

