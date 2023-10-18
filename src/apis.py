#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urequests as requests
import ujson as json

from config import OPENWEATHERMAP_API_KEY, OPENLUNAR_API_KEY

def get_lunar(url, date):
    lunar = {}
    r = requests.get(url + '?key={}&date={}'.format(OPENLUNAR_API_KEY, date))
    if r.content:
        try:
            content = json.loads(r.content)
            result = content['result']
            errno = content['error_code']
            if errno == 0:
                lunar['yangli'] = result['yangli']
                lunar['yinli'] = result['yinli']
                lunar['yi'] = result['yi']
                lunar['ji'] = result['ji']
                
                return lunar
            else:
                print('query error')
        except Exception as e:
            print('parse error')
    else:
        print('query error')


def get_weather_id(url):
    weather_ids = {}
    r = requests.get(url + '?key={}'.format(OPENWEATHERMAP_API_KEY))
    if r.content:
        try:
            content = json.loads(r.content)
            result = content['result']
            errno = content['error_code']
            if errno == 0:
                for el in result:
                    weather_ids[el['wid']] = el['weather']
                return weather_ids
            else:
                print('query error')
        except Exception as e:
            print('parse error')
    else:
        print('query error')


def get_weather(url, city, wids):
    weather = {}
    r = requests.get(url + '?key={}&city={}'.format(OPENWEATHERMAP_API_KEY, city))
    if r.content:
        try:
            content = json.loads(r.content)
            print(content)
            result = content['result']
            errno = content['error_code']
            if errno == 0:
                weather['city'] = city
                future = []
                for el in result['future']:
                    future.append({
                        'date': el['date'], 
                        'temperature': el['temperature'].strip('\u2103').split('/'), 
                        'weather': wids[el['wid']['day']],
                    })
                    
                weather['future'] = future
                return weather
            else:
                print('query error')
        except Exception as e:
            print('parse error')
    else:
        print('query error')

