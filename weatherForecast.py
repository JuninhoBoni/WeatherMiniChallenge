#!/usr/bin/env python3
#coding: utf-8
'''
PROGRAM NAME:   weatherForecast.py
VERSION:        1.0
DESCRIPTION:    WEATHER FORECAST IN THE NEXT FIVE DAYS; AIR HUMIDITY GREATER THAN 70%.
API:            https://openweathermap.org/forecast5
CHANGE:         V1.0 - 2020/05/21 - RELEASE                     - DIAS, DANIEL

'''
import sys, datetime
import requests #pip install requests
from datetime import timedelta

def getAPI():
    averageSum, humidity, dates = [0]*days, [0]*days, [0]*days
    index = 0
    lastDate = None
    response = requests.get('http://api.openweathermap.org/data/2.5/forecast?q={}&appid={}'.format(city, key))
    
    if response.status_code == 200:
        for list in response.json()['list']:
            #UTC + timezone
            dateTimezone = (datetime.datetime.strptime(list['dt_txt'], '%Y-%m-%d %H:%M:%S') + timedelta(seconds=response.json()['city']['timezone']))
            date = dateTimezone.strftime('%Y-%m-%d')
            
            if lastDate == None:
                lastDate = date
            
            if date != lastDate:
                humidity[index] = [humidity[index]/(averageSum[index]), 0][humidity[index] == 0]
                index+=1
                if index == days:
                    return humidity, dates
                lastDate = date
            
            dates[index] = dateTimezone
            averageSum[index] +=1
            humidity[index] += list['main']['humidity']
    else:
        print('API error return: {}'.format(response.status_code))
        sys.exit(1)

def messageCreator():
    humidityDays = []
    for i in range(days):
        if humidityAverage[i] > humidityGreater:
            humidityDays.append(dates[i].strftime('%A'))
    
    humidityDays[len(humidityDays)-1] = 'and ' + humidityDays[len(humidityDays)-1]
    week = (', '.join(humidityDays))

    if len(humidityDays) > 1:
        return('You should take an umbrella in these days: ' +  week.replace(', and', ' and'))
    elif len(humidityDays) == 1:
        return('You should take an umbrella:' + week.replace('and', ''))
    else:
        return("You shouldn't take an umbrella in the next few days.")

if __name__ == '__main__':
    city = 'Ribeirao Preto'
    days = 5
    humidityGreater = 70

    key = '1a4f67e9f28d756ca5380309833f4a78'
    humidityAverage, dates = getAPI()
    print(messageCreator())
    sys.exit(0)
    