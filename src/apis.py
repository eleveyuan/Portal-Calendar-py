#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urequests as requests
import ujson as json

from src.config import OPENWEATHERMAP_API_KEY, OPENLUNAR_API_KEY, WEATHER_URL, WEATHER_ID_URL, LUNAR_URL, DISTRICT
from src.time_utils import lunar_day_internal, day_internal
from src.birth import birthday, lunar_birthday


def zodiac_id(zodiac):
    zodiacs = ['\u9f20','\u725b','\u864e','\u5154','\u9f99','\u86c7','\u9a6c','\u7f8a','\u7334','\u9e21','\u72d7','\u732a']
    return zodiacs.index(zodiac)

def construct_multiline(words, ceil=6, word_lmt=15):
    words = words[:word_lmt]
    i = 1
    line, res ='', []
    for word in words:
        line += word + '.'
        i += 1
        if i > ceil:
            res.append(line.encode('utf8'))
            i = 1
            line = ''
    if len(line) > 0:
        res.append(line.encode('utf8'))

    return res

def get_lunar(date, url=LUNAR_URL):
    lunar = {}
    r = requests.get(url + '?key={}&date={}'.format(OPENLUNAR_API_KEY, date))
    if r.content:
        try:
            content = json.loads(r.content)
            result = content['result']
            errorno = content['error_code']
            if errorno == 0:
                birthday_coming = []
                if len(lunar_birthday) != 0:
                    for k, v in lunar_birthday.items():
                        err = lunar_day_internal(v, result['data']['lunar'])
                        if err is not None and err >= 0 and err <= 15:
                            birthday_coming.append({
                                k: (v, err)    
                            })
                if len(birthday) != 0:
                    for k, v in birthday.items():
                        err = day_internal(v, date)
                        if err is not None and err >= 0 and err <= 15:
                            birthday_coming.append({
                                k: (v, err)    
                            })

                lunar['weekday'] = result['data']['weekday']
                lunar['lunar_year'] = result['data']['lunarYear']
                lunar['zodiac_no'] = zodiac_id(result['data']['animalsYear'])
                lunar['zodiac'] = result['data']['animalsYear']
                lunar['lunar'] = result['data']['lunar']
                lunar['suit'] = construct_multiline(result['data']['suit'].strip('.').split('.'))
                lunar['avoid'] = construct_multiline(result['data']['avoid'].strip('.').split('.'))
                lunar['birth_coming'] = birthday_coming
                
                return lunar
            else:
                print('query error')
        except Exception as e:
            print(e)
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


def get_weather(wids, url=WEATHER_URL, city=DISTRICT):
    weather = {}
    r = requests.get(url + '?key={}&city={}'.format(OPENWEATHERMAP_API_KEY, city))
    if r.content:
        try:
            content = json.loads(r.content)
            result = content['result']
            errno = content['error_code']
            if errno == 0:
                weather['city'] = b'{}'.format(city)
                future = []
                for el in result['future']:
                    future.append({
                        'date': el['date'], 
                        'temperature': el['temperature'].strip('\u2103').split('/'), 
                        # 1: day, 0: night
                        'weather': {
                            1: el['wid']['day'],  # wids[el['wid']['day']].encode('utf8'),
                            0: el['wid']['night']  # wids[el['wid']['night']].encode('utf8')
                        },
                    })
                weather['future'] = future
                return weather
            else:
                print('query error')
        except Exception as e:
            print('parse error')
    else:
        print('query error')

def parse_weather_condition_id(_id):
    if _id == "00":
        return "CLEAR"  # 晴天
    elif _id == "01":
        return "FEW_CLOUDS"  # 多云
    elif _id == "02":
        return "OVERCAST_CLOUDS"  # 阴天
    elif _id == "03":
        return "SHOWERS"  # 阵雨
    elif _id in ["07", "08", "09", "10", "11", "12", "21", "22", "23", "24", "25"]:
        return "RAINS"  # 雨天
    elif _id in ["04", "05"]:
        return "THUNDERSTORMS"  # 雷雨
    elif _id in ["06", "13", "14", "15", "16", "17", "19", "26", "27", "28"]:
        return "SNOW"  # 雪天
    elif _id in ["18", "53"]:
        return "FOG"  # 雾霾
    else:
        return "UNKOWN"
    