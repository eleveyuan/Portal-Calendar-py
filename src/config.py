#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
wifi连接配置
"""
WIFI_NAME = ""
WIFI_PASS = ""
HOSTNAME = ""

"""
展示日期
"""
SHOW_DAY = True
SHOW_MONTH = True

LANGUAGE = "zh-cn"  # en-us

"""
时区
"""
TIME_ZONE = "Asia/Shanghai"


"""
api key
    OPENWEATHERMAP_API_KEY: 天气api
    OPENLUNAR_API_KEY: 黄历api
"""
OPENWEATHERMAP_API_KEY = ""
OPENLUNAR_API_KEY = ""

"""
1: 展示五天的天气预报
2: 展示当天3小时内的天气情况
"""
WEATHER_DISPLAY_TYPE = 1

SECONDARY_WEATHER_INFORMATION = 1
WEATHER_UNITS = "imperial"
WEATHER_LOCATION = ""
WEATHER_START_HOUR = 9


"""
    You probably don't need to edit anything below here
"""

"""
NTP(网络时间协议Network Time Protocol)服务器
    中国科学院国家授时中心: ntp.ntsc.ac.cn
    阿里云授时服务器: ntp.aliyun.com
    清华大学: ntp.tuna.tsinghua.edu.cn
"""
NTP_SERVERS = ["ntp.ntsc.ac.cn", "ntp.aliyun.com", "ntp.tuna.tsinghua.edu.cn", "time.google.com"]
TIMEZONED_SERVERS = [""]


"""
NTP服务请求，超时时间
"""
NTP_TIMEOUT_SECONDS = 5

"""
时区查找，超时时间
"""
TZ_LOOKUP_TIMEOUT_SECONDS = 5

"""
控制在午夜之前多久唤醒处理器以进行第一次和第二次 NTP 同步。

每天执行两次 NTP 同步，因为 ESP32 中的内部时钟非常不准确。

第一个时间应设置为您期望内部时钟在一天内关闭的最大可能时间，因为它将休眠一整天并在此时被唤醒。 
第二个应该设置为第一次同步和午夜之间的时间漂移的最大可能量。

如果时钟每天运行速度快+MINUTES_BEFORE_MIDNIGHT_TO_SYNC_1，那么实际上它将在午夜前 
MINUTES_BEFORE_MIDNIGHT_TO_SYNC_1 * 2 分钟被唤醒，这是 NTP 测量被认为可接受的
最长持续时间。 如果超过这个速度，每天都会发生多个第一阶段 NTP 同步，这会浪费电池。

如果时钟每天运行速度慢 -MINUTES_BEFORE_MIDNIGHT_TO_SYNC_1，那么它将在午夜准确唤醒并同步。 
任何比这慢的速度，它都不会在午夜准时醒来，并且日期转换也会延迟。

默认值对应于 ESP32 数据表中指定的最大不准确度，我建议您不要碰它们。(google翻译)
"""
MINUTES_BEFORE_MIDNIGHT_TO_SYNC_1 = 72
MINUTES_BEFORE_MIDNIGHT_TO_SYNC_2 = 8

"""
在显示错误之前，我们会多少小时没有互联网。 最好不要超过1天，
因为 ESP32 中的内部时钟通常每天会有两位数分钟的偏差。（google翻译。。还是自己改改）
"""
ERROR_AFTER_HOURS_WITHOUT_INTERNET = 24

"""
测量系统时钟的漂移并应用校正因子以获得更准确的计时。
 
由于 ESP32 的内部时钟会根据温度发生较大的漂移，因此假设时钟放置在温度相对稳定的环境中，
这对于提高时钟精度非常有效。
"""
MAX_RTC_CORRECTION_FACTOR = 0.025

"""
端口使用
"""
NTP_LOCAL_PORT_START = 4242
TIMEZONED_LOCAL_PORT_START = 2342

"""
引脚使用
"""
SPI_BUS = HSPI
DIN_PIN = -1  # COPI
CLK_PIN = -1  # SCK
CS_PIN = 15  # CS
DC_PIN = 23  # Any OUTPUT pin
RESET_PIN = 33  # Any OUTPUT pin
BUSY_PIN = 27  # Any INPUT pin

"""
时间相关，原项目global.h文件内容
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