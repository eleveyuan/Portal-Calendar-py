#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import WIFI_NAME, TIME_ZONE, WEATHER_LOCATION


def error(msg):
    pass


def errorNoWifi():

    error("""NO WIFI CONNECTION

        Your WiFi network is either down, out of range,
        or you entered the wrong password.
        WiFi Name: {}
        """.format(WIFI_NAME))

def errorNtpFailed():

    error("""NO INTERNET CONNECTION
          
        Your WiFi network works, but the NTP servers didn't
        respond. This probably means your WiFi has no internet
        connection. Or, you configured the NTP servers yourself,
        in which case you might have messed something up.
        """)


def errorTzLookupFailed():
    error("""TIMEZONE LOOKUP FAILED
          
        Your timezone is either invalid, or the timezone servers
        are down. If you configured the timezone servers
        yourself, you might have messed something up.
          
        Your timezone: {}
        """.format(TIME_ZONE))
    
def errorInvalidApiKey():

    error("""INVALID API KEY
          
          OpenWeatherMap.org says your API key is invalid.
          You probably have an issue with your configuration.
          Go to your account -> My API Keys and make sure
          the one there matches the one you entered. Or, just
          disable the weather feature entirely.
        """)


def errorInvalidLocation():
    
    error("""INVALID WEATHER LOCATION
          
        OpenWeatherMap.org couldn't find any results
        for the weather location you entered. You
        probably have an issue with your configuration.
          
        You Location: {}
        """.format(WEATHER_LOCATION))
    
