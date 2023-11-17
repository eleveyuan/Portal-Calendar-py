import gc
import network
import utime
from time import sleep_ms
from machine import SPI, Pin

from src.config import *
from src.Display import Display
from src.time_utils import settime, strftime


display = Display()

wlan = network.WLAN(network.STA_IF)

def start_wifi():
    wlan.active(False)
    if wlan.isconnected():
        return True
    
    if WIFI_PASS != '':
        wlan.active(True)
        wlan.scan()
        wlan.connect(WIFI_NAME, WIFI_PASS)
        while not wlan.isconnected():
            pass
    else:
        wlan.connect(WIFI_NAME, '')
    
    if wlan.isconnected():
        return True


def stop_wifi():
    if wlan.isconnected():
        wlan.disconnect()
        wlan.active(False)
        

def setup():
    if start_wifi():
        print(wlan.isconnected())
        
        # Sync timezone
        settime(TIME_ZONE, NTP_SERVERS)
        date_fmt = strftime(utime.localtime(), 0)
        year, month, mday, hour, minute, second, weekday, yearday = utime.localtime()
        
        display.update(date_fmt)
    
    stop_wifi()
    
setup()
gc.collect()
print(gc.mem_free()) 