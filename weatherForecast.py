#!/usr/bin/env python3
#coding: utf-8
'''
PROGRAM NAME:   weatherForecast.py
VERSION:        2.0
DESCRIPTION:    WEATHER FORECAST IN THE NEXT FIVE DAYS; AIR HUMIDITY GREATER THAN 70%.
API:            https://openweathermap.org/forecast5
CHANGE:         V1.0 - 2020/05/21 - RELEASE                     - DIAS, DANIEL
                V2.0 - 2020/05/25 - GLOBAL CITIES
                                  - IMPROVEMENTS
                                  - COMMENTS
                                  - EXCEPTIONS
                                  - VALIDATIONS                 - DIAS, DANIEL

'''
import sys, datetime
import requests #pip install requests
from datetime import timedelta

#Custom class of exceptions
class Error(Exception):
    pass

class CustomError(Error):
    def __init__(self, message):
        self.message = message

#Function validate variables
def validate_variables():
    try:
        if days <= 0:
            raise CustomError("Variable 'day' is less than 0. Inform value above zero.")
        if not (0 < humidityGreater < 100):
            raise CustomError("Variable 'humidityGreater' is out of range. Inform value between {min} and {max}.".format(min=0, max=100))
    except CustomError as ex:
        print(ex)
        sys.exit(1)
    except Exception:
        print('Enter numbers only.')
        sys.exit(2)

#Function API Request
def get_api():
    #Local variables
    humidityData = []
    index = -1
    lastDate = None

    try:
        #API request
        response = requests.get('http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={key}'.format(city=city, key=key))
        #Error 404
        if response.status_code == 404:
            raise CustomError('API error return: {error}. Please check the name of the city.'.format(error=response.status_code))
        #Error 401
        if response.status_code == 401:
            raise CustomError('API error return: {error}. Please check the API key.'.format(error=response.status_code))
        #Other errors
        elif response.status_code != 200:
            raise CustomError('API error return: {error}'.format(error=response.status_code))
    #Exceptions messages on the screen
    except CustomError as ex:
        print(ex)
        sys.exit(3)
    except Exception:
        print('Connection error occurred, please check your internet connection and request link.')
        sys.exit(4)

    for list in response.json()['list']:
        #Convert time UTC + timezone
        dateTimezone = (datetime.datetime.strptime(list['dt_txt'], '%Y-%m-%d %H:%M:%S') + timedelta(seconds=response.json()['city']['timezone']))
        #print('{}|{}'.format(list['main']['humidity'], str(dateTimezone)[:10])) #TEST
        
        #Test if the day is different
        if lastDate == None or not str(dateTimezone).count(str(lastDate)[:10]):
            index+=1
            lastDate = dateTimezone
        
        #If it is the first run, add first value
        try:
            humidityData[index][0] += list['main']['humidity']
            humidityData[index][1] +=1
            humidityData[index][2] = dateTimezone
        except IndexError:
            humidityData.append([list['main']['humidity'], 1, dateTimezone])
    #print(humidityData) #TEST
    
    #Retorna as variáveis
    return humidityData

#Function Message Creator
def message_creator():
    #Local Variable
    humidityDays = []

    #Weekday
    for i in range(days):
        try:
            if (humidityData[i][0] / humidityData[i][1]) > humidityGreater:
                humidityDays.append(humidityData[i][2].strftime('%A'))
        except IndexError:
            print('Weather forecast available only up to {days} days. Please change the variable days.'.format(days=i))
            sys.exit(2)

    #A few days
    if len(humidityDays) > 1:
        humidityDays[len(humidityDays)-1] = 'and ' + humidityDays[len(humidityDays)-1]
        week = (', '.join(humidityDays))
        return('You should take an umbrella in these days: ' +  week.replace(', and', ' and'))
    
    #Only one day
    elif len(humidityDays) == 1:
        return('You should take an umbrella: ' + (', '.join(humidityDays)))
    
    else:
        return("You shouldn't take an umbrella in the next few days.")

if __name__ == '__main__':
    key = '1a4f67e9f28d756ca5380309833f4a78'
    city = 'Ribeirao Preto'
    days = 5
    humidityGreater = 70
    validate_variables()
    humidityData = get_api()
    print(message_creator())
    sys.exit(0)
    