#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    import usocket as socket
except:
    import socket
try:
    import ustruct as struct
except:
    import struct

NTP_DELTA = 3155673600


def time(host):
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1b
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(2)
    res = s.sendto(NTP_QUERY, addr)
    msg = s.recv(48)
    s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    return val - NTP_DELTA


# There's currently no timezone support in MicroPython, so
# utime.localtime() will return UTC time (as if it was .gmtime())
# add timezone org,default 8
def settime(timezone=8, servers=['ntp.ntsc.ac.cn']):
    import machine
    import utime
    for server in servers:
        t1= utime.ticks_ms()
        t = 0
        while utime.ticks_diff(utime.ticks_ms(), t1) < 5000:
            try:
                t = time(server)
            except OSError as e:
                pass
            else:
                break
        if t != 0:  # a naive way
            break
    t = t + (timezone * 60 * 60)
    tm = utime.localtime(t)
    tm = tm[0:3] + (0, ) + tm[3:6] + (0, )
    machine.RTC().datetime(tm)
    print(utime.localtime())


def get_days_in_month(month, year):
    if month == 2:
        return 29 if ((year % 4 == 0 and year % 100 != 0 ) or (year % 400 == 0)) else 28
    elif month in (4, 6, 9, 11):
        return 30
    else:
        return 31