#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
wifi info
"""
WIFI_NAME = "Mi 10"
WIFI_PASS = "12345688"
HOSTNAME = ""

LANGUAGE = "zh-cn"  # en-us
TIME_ZONE = "Asia/Shanghai"
CITY = ""
DISTRICT = ""

"""
PINS
"""
DIN_PIN = 11  # COPI
CLK_PIN = 12  # SCK
CS_PIN = 10  # CS
DC_PIN = 13  # Any OUTPUT pin
RESET_PIN = 1  # Any OUTPUT pin
BUSY_PIN = 3  # Any INPUT pin

"""
api key
    OPENWEATHERMAP_API_KEY: 天气api
    OPENLUNAR_API_KEY: 黄历api
"""
WEATHER_URL = "http://apis.juhe.cn/simpleWeather/query"
WEATHER_ID_URL = "http://apis.juhe.cn/simpleWeather/wids"
OPENWEATHERMAP_API_KEY = ""
LUNAR_URL = "http://v.juhe.cn/calendar/day"
OPENLUNAR_API_KEY = ""


"""
    You probably don't need to edit anything below here
"""

"""
NTP servers
    中国科学院国家授时中心: ntp.ntsc.ac.cn
    阿里云授时服务器: ntp.aliyun.com
    清华大学: ntp.tuna.tsinghua.edu.cn
"""
TIME_ZONE = 8
NTP_SERVERS = ["ntp.ntsc.ac.cn", "ntp.aliyun.com", "ntp.tuna.tsinghua.edu.cn", "time.google.com"]
TIMEZONED_SERVERS = [""]
NTP_TIMEOUT_SECONDS = 5
TZ_LOOKUP_TIMEOUT_SECONDS = 5

"""
 Controls how long before midnight the processor is woken up for the first and second NTP syncs.
 
 Two NTP syncs per day are performed per day because the internal clock in the ESP32 is very inaccurate.
 
 The first time should be set to the maximum possible amount you expect the internal clock to be off in one day, since it will sleep for an entire day
 and be woken at this time. The second one should be set to the maximum possible amount it will drift in the time betwen the first sync and midnight.
 
 If the clock is running +MINUTES_BEFORE_MIDNIGHT_TO_SYNC_1 fast per day, then in reality it will be woken up MINUTES_BEFORE_MIDNIGHT_TO_SYNC_1 * 2
 minutes before midnight, which is the maximum duration the NTP measurement will be deemed acceptable for. Any faster than that, and multiple
 first stage NTP syncs will happen per day, which wastes battery.
 
 If the clock is running -MINUTES_BEFORE_MIDNIGHT_TO_SYNC_1 slow per day, then it will wake up and sync exactly at midnight. Any slower than that,
 and it won't wake wake up in time for midnight and the date changeover will be late.
 
 The default values correspond to the maximum inaccuracy specified in the ESP32's datasheet, I recommend you don't touch them.
"""
MINUTES_BEFORE_MIDNIGHT_TO_SYNC_1 = 72
MINUTES_BEFORE_MIDNIGHT_TO_SYNC_2 = 8

"""
 How many hours we'll go without internet before showing an error. This really shouldn't be longer than a couple days, since the internal
 clock in the ESP32 is usually off by double-digit minutes per day.
"""
ERROR_AFTER_HOURS_WITHOUT_INTERNET = 24

"""
 Measure drift in the system clock and apply a correction factor for more accurate timekeeping.
 
 Since the ESP32's internal clock drifts significantly based on temperature, this can be pretty effective at improving the clock's accuracy
 assuming the clock is placed in a relatively temperature-stable environment. Like, you know, indoors.
"""
MAX_RTC_CORRECTION_FACTOR = 0.025

"""
PORTS
"""
NTP_LOCAL_PORT_START = 4242
TIMEZONED_LOCAL_PORT_START = 2342

"""
TIME
"""
uS_PER_S = 1000000
SECONDS_PER_HOUR = 3600
SECONDS_PER_DAY = (SECONDS_PER_HOUR * 24)

# ERROR_RETRY_INTERVAL_SECONDS = ERROR_RETRY_INTERVAL_MINUTES * 60
ERROR_AFTER_SECONDS_WITHOUT_INTERNET = ERROR_AFTER_HOURS_WITHOUT_INTERNET * 3600
SECONDS_BEFORE_MIDNIGHT_TO_SYNC_1 = MINUTES_BEFORE_MIDNIGHT_TO_SYNC_1 * 60
SECONDS_BEFORE_MIDNIGHT_TO_SYNC_2 = MINUTES_BEFORE_MIDNIGHT_TO_SYNC_2 * 60
TZ_LOOKUP_TIMEOUT_MS = TZ_LOOKUP_TIMEOUT_SECONDS * 1000
NTP_TIMEOUT_MS = NTP_TIMEOUT_SECONDS * 1000