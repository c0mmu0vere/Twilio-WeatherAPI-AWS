"""
************************************************************************
* Author = Fabricio Moreira                                            *
* Date = '02/07/2023'                                                  *
* Description = Sending Twilio messages with Python                    *
************************************************************************
"""


import os
from twilio.rest import Client
from twilio_config import *
import time
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
import requests
from tqdm import tqdm
from datetime import datetime
from utils import request_wapi,get_forecast,prepare_summary,send_message,get_date


query = 'Argentina'
api_key = API_KEY_WAPI

input_date = get_date()
response = request_wapi(api_key,query)

data = []

for i in tqdm(range(24),colour = 'green'):

    data.append(get_forecast(response,i))

summary = prepare_summary(data, query)

# Send Message
message_id = send_message(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN, summary, PHONE_NUMBER, MY_NUMBER)


print('Message Sent ' + message_id)
