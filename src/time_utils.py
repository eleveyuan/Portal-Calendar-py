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
# changed: second paramater supports list of servers
# checked on wokwi ESP32 Simulator
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


def strftime(tm, full):
    if full:
        # only YYYY-MM-DD
        return '{:02}-{:02}-{:02}'.format(tm[0], tm[1], tm[2])
    else:
        # YYYY-MM-DD or YYYY-M-D
        # 2023-10-19 or 2021-1-1
        return '{}-{}-{}'.format(tm[0], tm[1], tm[2])


def day_internal(lunar1, lunar2):
    lunar_dt = [
        '\u4e00', '\u4e8c', '\u4e09', '\u56db', '\u4e94', '\u516d', '\u4e03', '\u516b', '\u4e5d', '\u5341',
        '\u5341\u4e00', '\u5341\u4e8c', '\u5341\u4e09', '\u5341\u56db', '\u5341\u4e94', '\u5341\u516d', '\u5341\u4e03', '\u5341\u516b', '\u5341\u4e5d',
        '\u4e8c\u5341', '\u4e8c\u5341\u4e00', '\u4e8c\u5341\u4e8c', '\u4e8c\u5341\u4e09', '\u4e8c\u5341\u56db', '\u4e8c\u5341\u4e94', '\u4e8c\u5341\u516d', '\u4e8c\u5341\u4e03', '\u4e8c\u5341\u516b', '\u4e8c\u5341\u4e5d', '\u4e09\u5341'
    ]
    llist1 = lunar1.replace('\u521d', '').split('\u6708')  # 初 \u521d
    llist2 = lunar2.replace('\u521d', '').split('\u6708')  # 月 \u6708
    if llist1[0] == llist2[0]:
        return lunar_dt.index(llist1[1]) - lunar_dt.index(llist2[1])
    else:
        return None
