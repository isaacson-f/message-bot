# python script for sending message update
from time import sleep
import pandas as pd
import clx.xms as sinch
from datetime import date, datetime, timedelta
import math
import os
from dotenv import load_dotenv, find_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))

absDIR = os.path.join(BASEDIR, '.env')

load_dotenv(absDIR)

api_key = os.environ["api-token"]
print(api_key)
secret = os.environ["secret-key"]
print(secret)
phone_number = os.environ["phone-number"]
print(phone_number)

duties = ['Door', 'Bar', 'Event Monitor', 'Setup', 'Cleanup']
event_start_time = datetime(2022, 8, 12, 22)
monitor_start_time = datetime(2022, 8, 12, 20, 30)
setup_start_time = datetime(2022, 8, 12, 20)
cleanup_start_time = datetime(2022, 8, 13, 9)

def time_to_end(start_time, length_of_event):
    minutes_length = 0
    if length_of_event % 30 is 0:
        minutes_length = length_of_event % 60
        length_of_event = math.floor(length_of_event / 60)
    finish_time = start_time + timedelta(hours=length_of_event, minutes = minutes_length)
    return start_time, finish_time

def sendDuties():
    with open('Book1.csv','r') as excel:
        file = pd.read_csv(excel)
        duty_dict = {}
        print(len(file))
        for i, duty in enumerate(duties):
            for i in range(0, len(file)):
                if duty is 'Door' or duty is 'Bar':
                    start_time = time_to_end(event_start_time, 30 * (i+1))
                if duty is 'Event Monitor':
                    start_time = time_to_end(monitor_start_time, 3)
                if duty is 'Setup':
                    start_time = time_to_end(setup_start_time, 1)
                if duty is 'Cleanup':
                    start_time = time_to_end(cleanup_start_time, 2)
                current_duties = duty_dict.get(file[duty][i])
                if current_duties is None:
                    current_duties = {}
                current_duties[duty] = [start_time[0], start_time[1]]
                duty_dict[file[duty][i]] =  current_duties
        print(duty_dict)
    print(start_time)
# function for sending SMS
def sendSMS(name, number, message):

	# enter all the details
	# get app_key and app_secret by registering
	# a app on sinchSMS
    client = sinch.Client(secret, api_key)

    try:
        batch_params = sinch.api.MtBatchTextSmsCreate()
        batch_params.sender = phone_number
        batch_params.recipients = ['9523530315']
        batch_params.body = 'Hello, ${name}!'
        batch_params.parameters = {
                'name': {
                    '9523530315': 'Ethan',
                    'default': 'valued customer'
                }
            }

        batch = client.create_batch(batch_params)
        print('The batch was given ID %s' % batch.batch_id)
    except Exception as ex:
        print('Error creating batch: %s' % str(ex))

if __name__ == "__main__":
	sendSMS('Ethan',9523530315, "hello")

