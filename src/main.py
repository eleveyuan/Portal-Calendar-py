#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    相当于原项目 portal-calender.ino 文件，也即入口文件
"""
import network

from config import *


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.scan()

def startWifi():
    if wlan.isconnected():
        return True
    
    if WIFI_PASS != '':
        wlan.connect(WIFI_NAME, WIFI_PASS)
    else:
        wlan.connect(WIFI_NAME, '')
    
    if wlan.isconnected():
        return True


def stopWifi():
    pass
