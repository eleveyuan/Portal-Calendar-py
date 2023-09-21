#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import LANGUAGE


if LANGUAGE == 'zh-cn':

    I18N_MONTHS = [
        '一月',
        '二月',
        '三月',
        '四月',
        '五月',
        '六月',
        '七月',
        '八月',
        '九月',
        '十月',
        '十一月',
        '十二月'
    ]


    I18N_DAYS = [
        '星期一',
        '星期二',
        '星期三',
        '星期四',
        '星期五',
        '星期六',
        '星期日'
    ]

    I18N_DAYS_ABBREVIATIONS = [
        '周一',
        '周二',
        '周三',
        '周四',
        '周五',
        '周六',
        '周日'
    ]

else:

    I18N_MONTHS = [
        "JANUARY",
        "FEBRUARY",
        "MARCH",
        "APRIL",
        "MAY",
        "JUNE",
        "JULY",
        "AUGUST",
        "SEPTEMBER",
        "OCTOBER",
        "NOVEMBER",
        "DECEMBER",
    ]

    I18N_DAYS = [
        "SUNDAY",
        "MONDAY",
        "TUESDAY",
        "WEDNESDAY",
        "THURSDAY",
        "FRIDAY",
        "SATURDAY",
    ]

    I18N_DAYS_ABBREVIATIONS = [
        "SUN",
        "MON",
        "TUE",
        "WED",
        "THU",
        "FRI",
        "SAT",
    ]

