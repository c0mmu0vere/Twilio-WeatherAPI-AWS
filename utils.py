
import pandas as pd
from twilio.rest import Client
from twilio_config import PHONE_NUMBER, MY_NUMBER
from datetime import datetime
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

def get_date():

    input_date = datetime.now()
    input_date = input_date.strftime("%Y-%m-%d")

    return input_date

def request_wapi(api_key,query):

    url_clima = 'http://api.weatherapi.com/v1/forecast.json?key='+api_key+'&q='+query+'&days=1&aqi=no&alerts=no'

    try :
        response = requests.get(url_clima).json()
    except Exception as e:
        print(e)

    return response

def get_forecast(response,i):
    
    date = response['forecast']['forecastday'][0]['hour'][i]['time'].split()[0]
    time = int(response['forecast']['forecastday'][0]['hour'][i]['time'].split()[1].split(':')[0])
    condition = response['forecast']['forecastday'][0]['hour'][i]['condition']['text']
    temp_c = float(response['forecast']['forecastday'][0]['hour'][i]['temp_c'])
    will_it_rain = response['forecast']['forecastday'][0]['hour'][i]['will_it_rain']
    chance_of_rain = response['forecast']['forecastday'][0]['hour'][i]['chance_of_rain']
    
    return date,time,condition,temp_c,will_it_rain, chance_of_rain

def prepare_summary(data, query):

    col = ['Date','Time','Condition','Temperature','Rain','rain_chance']
    df = pd.DataFrame(data,columns=col)
    df = df.sort_values(by = 'Time',ascending = True)

    today = df['Date'][0]
    temp_max = df['Temperature'].max()
    temp_min = df['Temperature'].min()
    rain_hours = df[(df['Rain']==1)]
    rain_hours = ', '.join(str(x) for x in rain_hours['Time'])

    if df['Condition'].value_counts().idxmax() == 'Clear':
        day_forecast = df['Condition'].value_counts().idxmax() + ' ' + str(chr(0x1F308))
    elif df['Condition'].value_counts().idxmax() == 'Partly cloudy':
        day_forecast = df['Condition'].value_counts().idxmax() + ' ' + str(chr(0x26C5))
    elif df['Condition'].value_counts().idxmax() == 'Sunny':
        day_forecast = df['Condition'].value_counts().idxmax() + ' ' + str(chr(0x2600))
    elif df['Condition'].value_counts().idxmax() == 'Patchy rain possible':
        day_forecast = df['Condition'].value_counts().idxmax() + ' ' + str(chr(0x1F326))

    summary = f"Summary of weather for Buenos Aires, {query}:\n" \
        f"Date: {today} {chr(0x1F4C5)}\n" \
        f"The maximum temperature will be: {temp_max} °C {chr(0x1F4C8)}\n" \
        f"The minimum temperature will be: {temp_min} °C {chr(0x1F4C9)}\n" \
        f"Today's forecast is: {day_forecast}\n" \
        f"The hours at which rain is forecast will be: {rain_hours if rain_hours else 'None'} {chr(0x2614)}\n" \

    return summary

def send_message(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN, summary):

    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN

    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body=summary,
                        from_=PHONE_NUMBER,
                        to=MY_NUMBER
                    )

    return message.sid
