#!/usr/bin/env python
# -*- coding: utf-8 -*-

def encode_get_utf8_size(utf):
    if utf < 0x80:
        return 1
    if utf >= 0x80 and utf < 0xC0:
        return -1
    if utf >= 0xC0 and utf < 0xE0:
        return 2
    if utf >= 0xE0 and utf < 0xF0:
        return 3
    if utf >= 0xF0 and utf < 0xF8:
        return 4
    if utf >= 0xF8 and utf < 0xFC:
        return 5
    if utf >= 0xFC:
        return 6

def encode_utf8_to_unicode(utf8):
    utfbytes = encode_get_utf8_size(utf8[0])
    if utfbytes == 1:
        unic = utf8[0]
    if utfbytes == 2:
        b1 = utf8[0]
        b2 = utf8[1]
        if ((b2 & 0xE0) != 0x80):
            return -1
        unic = ((((b1 << 6) + (b2 & 0x3F)) & 0xFF) << 8) | (((b1 >> 2) & 0x07) & 0xFF)
    if utfbytes == 3:
        b1 = utf8[0]
        b2 = utf8[1]
        b3 = utf8[2]
        if (((b2 & 0xC0) != 0x80) or ((b3 & 0xC0) != 0x80)):
            return -1
        unic = ((((b1 << 4) + ((b2 >> 2) & 0x0F)) & 0xFF) << 8) | (((b2 << 6) + (b3 & 0x3F)) & 0xFF)

    if utfbytes == 4:
        b1 = utf8[0]
        b2 = utf8[1]
        b3 = utf8[2]
        b4 = utf8[3]
        if (((b2 & 0xC0) != 0x80) or ((b3 & 0xC0) != 0x80) or ((b4 & 0xC0) != 0x80)):
            return -1
        unic = ((((b3 << 6) + (b4 & 0x3F)) & 0xFF) << 16) | ((((b2 << 4) + ((b3 >> 2)
                                                                  & 0x0F)) & 0xFF) << 8) | ((((b1 << 2) & 0x1C) + ((b2 >> 4) & 0x03)) & 0xFF)
    if utfbytes == 5:
        b1 = utf8[0]
        b2 = utf8[1]
        b3 = utf8[2]
        b4 = utf8[3]
        b5 = utf8[4]
        if (((b2 & 0xC0) != 0x80) or ((b3 & 0xC0) != 0x80) or ((b4 & 0xC0) != 0x80) or ((b5 & 0xC0) != 0x80)):
            return -1
        unic = ((((b4 << 6) + (b5 & 0x3F)) & 0xFF) << 24) | (((b3 << 4) + ((b4 >> 2) & 0x0F) & 0xFF) << 16) | ((((b2 << 2) + ((b3 >> 4) & 0x03)) & 0xFF) << 8) | (((b1 << 6)) & 0xFF)
    if utfbytes == 6:
        b1 = utf8[0]
        b2 = utf8[1]
        b3 = utf8[2]
        b4 = utf8[3]
        b5 = utf8[4]
        b6 = utf8[5]

        if (((b2 & 0xC0) != 0x80) or ((b3 & 0xC0) != 0x80) or ((b4 & 0xC0) != 0x80) or ((b5 & 0xC0) != 0x80) or ((b6 & 0xC0) != 0x80)):
            return -1

        unic = ((((b5 << 6) + (b6 & 0x3F)) << 24) & 0xFF) | (((b5 << 4) + ((b6 >> 2) & 0x0F) << 16) & 0xFF) | ((((b3 << 2) + ((b4 >> 4) & 0x03)) << 8) & 0xFF) | ((((b1 << 6) & 0x40) + (b2 & 0x3F)) & 0xFF)

    return unic


def is_space_char(utf):
    return cp == 0x9 or cp == 0x20 or cp == 0xA0
