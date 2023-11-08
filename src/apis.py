#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urequests as requests
import ujson as json

from config import OPENWEATHERMAP_API_KEY, OPENLUNAR_API_KEY, WEATHER_URL, WEATHER_ID_URL, LUNAR_URL


def get_lunar(date, url=LUNAR_URL):
    lunar = {}
    r = requests.get(url + '?key={}&date={}'.format(OPENLUNAR_API_KEY, date))
    if r.content:
        try:
            content = json.loads(r.content)
            result = content['result']
            errorno = content['error_code']
            if errorno == 0:
                lunar['weekday'] = result['data']['weekday']
                lunar['lunar_year'] = result['data']['lunarYear']
                lunar['zodiac'] = result['data']['animalsYear']
                lunar['lunar'] = result['data']['lunar']
                lunar['suit'] = result['data']['suit']
                lunar['avoid'] = result['data']['avoid']
                
                return lunar
            else:
                print('query error')
        except Exception as e:
            print('parse error')
    else:
        print('query error')


def get_weather_id(url=WEATHER_ID_URL):
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


def get_weather(wids, url=WEATHER_URL, city='曲江'):
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
                        # 1: day, 0: night
                        'weather': { 1: wids[el['wid']['day']], 0: wids[el['wid']['night']]},
                    })
                weather['future'] = future
                return weather
            else:
                print('query error')
        except Exception as e:
            print('parse error')
    else:
        print('query error')

def parse_weather_condition_id(id):
    if id == "00":
        return "CLEAR"  # 晴天
    elif id == "01":
        return "FEW_CLOUDS"  # 多云
    elif id == "02":
        return "OVERCAST_CLOUDS"  # 阴天
    elif id == "03":
        return "SHOWERS"  # 阵雨
    elif id in ["07", "08", "09", "10", "11", "12", "21", "22", "23", "24", "25"]:
        return "RAINS"  # 雨天
    elif id in ["04", "05"]:
        return "THUNDERSTORMS"  # 雷雨
    elif id in ["06", "13", "14", "15", "16", "17", "19", "26", "27", "28"]:
        return "SNOW"  # 雪天
    elif id in ["18", "53"]:
        return "FOG"  # 雾霾
    else:
        return "UNKOWN"
    