#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.config import LANGUAGE

I18N_MONTHS, I18N_DAYS, I18N_DAYS_ABBREVIATIONS = [], [], []

if LANGUAGE == 'zh-cn':

    I18N_MONTHS = [
        b'一月',
        b'二月',
        b'三月',
        b'四月',
        b'五月',
        b'六月',
        b'七月',
        b'八月',
        b'九月',
        b'十月',
        b'十一月',
        b'十二月'
    ]


    I18N_DAYS = [
        b'星期一',
        b'星期二',
        b'星期三',
        b'星期四',
        b'星期五',
        b'星期六',
        b'星期日'
    ]

    I18N_DAYS_ABBREVIATIONS = [
        b'周一',
        b'周二',
        b'周三',
        b'周四',
        b'周五',
        b'周六',
        b'周日'
    ]

else:

    I18N_MONTHS = [
        b"JANUARY",
        b"FEBRUARY",
        b"MARCH",
        b"APRIL",
        b"MAY",
        b"JUNE",
        b"JULY",
        b"AUGUST",
        b"SEPTEMBER",
        b"OCTOBER",
        b"NOVEMBER",
        b"DECEMBER",
    ]

    I18N_DAYS = [
        b"SUNDAY",
        b"MONDAY",
        b"TUESDAY",
        b"WEDNESDAY",
        b"THURSDAY",
        b"FRIDAY",
        b"SATURDAY",
    ]

    I18N_DAYS_ABBREVIATIONS = [
        b"SUN",
        b"MON",
        b"TUE",
        b"WED",
        b"THU",
        b"FRI",
        b"SAT",
    ]

