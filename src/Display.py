#!/usr/bin/env python
# -*- coding: utf-8 -*-
import utime as time

import DisplayEPD7in5

from time_utils import get_days_in_month, is_day_light
from I18N import I18N_MONTHS, I18N_DAYS, I18N_DAYS_ABBREVIATIONS
from apis imoprt get_weather_id, get_weather, get_lunar, parse_weather_condition_id

from resource.error import IMG_ERROR
from resource.smiley16px import FONT_SMILEY16
from resource.smiley24px import FONT_SMILEY24
from resource.smiley32px import FONT_SMILEY32
from resource.smiley256px import FONT_SMILEY256

from resource.weather_frame import IMG_WEATHER_FRAME
from resource.weather_frame_empty import IMG_WEATHER_FRAME_EMPTY
from resource.weather_cloudy import IMG_WEATHER_CLOUDY
from resource.weather_day_clear import IMG_WEATHER_DAY_CLEAR
from resource.weather_night_clear import IMG_WEATHER_NIGHT_CLEAR
from resource.weather_partly_cloudy_day import IMG_WEATHER_PARTLY_CLOUDY_DAY
from resource.weather_partly_cloudy_night import IMG_WEATHER_PARTLY_CLOUDY_NIGHT
from resource.weather_scattered_showers_day import IMG_WEATHER_SCATTERED_SHOWERS_DAY
from resource.weather_scattered_showers_night import IMG_WEATHER_SCATTERED_SHOWERS_NIGHT
from resource.weather_showers import IMG_WEATHER_SHOWERS
from resource.weather_thunderstorms import IMG_WEATHER_THUNDERSTORMS
from resource.weather_fog import IMG_WEATHER_FOG
from resource.weather_snow import IMG_WEATHER_SNOW
from resource.weather_info_degree_symbol import IMG_WEATHER_INFO_DEGREE_SYMBOL
from resource.weather_info_percent_symbol import IMG_WEATHER_INFO_PERCENT_SYMBOL

H_CENTER = 225
ICON_SIZE = 64
ICON_SPACING = 9
LEFT =  82
RIGHT = LEFT + ICON_SIZE * 5 + ICON_SPACING * 4
WIDTH = RIGHT - LEFT
ICON_TOP = 550


class Display:
    def __init__():
        fb_size = int(DisplayEPD7in5.EPD_WIDTH * DisplayEPD7in5.EPD_HEIGHT / 8)
        self.frame_black = bytearray(fb_size)
        self.frame_red = bytearray(fb_size)
    
    def init():
        self._display = DisplayEPD7in5.DisplayEPD7in5(spi, cs=10, dc=13, rst=1, busy=3) 
        self._display.set_rotation(epd.ROTATION_270)

    def error(self, msg, will_retry):
        # show error message
        self.init()
        y = self._display.get_height() - self._display.get_height() / 1.618
        self._display.draw_image(self.frame_black, H_CENTER, y, IMG_ERROR, black, DisplayEPD7in5.BOTTOM_CENTER)
        self._display.draw_multiline_text(self.frame_black, H_CENTER, y + FONT_SMILEY24.ascent + FONT_SMILEY24.descent, msg, FONT_SMILEY24, black, DisplayGDEW075T7.TOP_CENTER)

        if will_retry:
            self._display.draw_multiline_text(self.frame_black, H_CENTER, self._display.get_height() - 12, [
            "Will try again in 1 hour. Or, press the RESET button",
            "on the back of the device to retry now."
            ], FONT_SMILEY24, black, DisplayGDEW075T7.BOTTOM_CENTER)
        
        self._display.display(self.frame_black)

    def update(self):
        self.init()

        year = time.localtime()[0]
        month = time.localtime()[1]
        day = time.localtime()[2]
        days_in_month = get_days_in_month(month, year)

        # static lines
        self._display.draw_hline(self.frame_black, LEFT, 50, WIDTH, 2, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)
        self._display.draw_hline(self.frame_black, LEFT, 430, WIDTH, 2, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)
        self._display.draw_hline(self.frame_black, LEFT, 538, WIDTH, 2, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)

        # family logo

        # show BIG Date
        line = b'{}'.format(day)
        self._display.draw_text(self.frame_black, line, LEFT, 16, FONT_SMILEY256, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT, 10)
        
        # show zodiac pic

        # show small date
        line = b'{}/{}'.format(month, day)
        self._display.draw_text(self.frame_black, line, LEFT, 394, FONT_SMILEY32, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)

        # show day name
        self._display.draw_text(self.frame_black, I18N_DAYS[time.localtime()[6]], RIGHT, 394, FONT_SMILEY32, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_RIGHT)
        # show month name
        self._display.draw_text(self.frame_black, I18N_MONTHS[month], LEFT, 14, FONT_SMILEY32, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)
        # show year
        self._display.draw_text(self.frame_black, b'{}'.format(year), RIGHT, 14, FONT_SMILEY32, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_RIGHT)

        # show lunar info
        # show birthday info

        # show weather
        wids = get_weather_id
        weathers = get_weather(wids)
        i = 0
        for weather in weathers['future']:
            self.draw_daily_weather(weather, i)
            i += 1

    def get_weather_condition_icon(self, condition, day):
        if condition == "CLEAR":
            return IMG_WEATHER_DAY_CLEAR if day else IMG_WEATHER_NIGHT_CLEAR
        elif condition == "FEW_CLOUDS":
            return IMG_WEATHER_PARTLY_CLOUDY_DAY if day else IMG_WEATHER_PARTLY_CLOUDY_NIGHT
        elif condition == "OVERCAST_CLOUDS":
            return IMG_WEATHER_CLOUDY
        elif condition == "SHOWERS":
            return IMG_WEATHER_SCATTERED_SHOWERS_DAY if day else IMG_WEATHER_SCATTERED_SHOWERS_NIGHT
        elif condition == "RAINS":
            return IMG_WEATHER_SHOWERS
        elif condition == "THUNDERSTORMS":
            return IMG_WEATHER_THUNDERSTORMS
        elif condition == "SNOW":
            return IMG_WEATHER_SNOW
        elif condition == "FOG":
            return IMG_WEATHER_FOG
        else:
            return None

    def draw_weather_info_text(self, text, symbol, x, y):
        text_width = self._display.measure_text(text, FONT_SMILEY24)
        x -= (text_width + symbol['width'] // 2) // 2
        self._display.draw_text(self.frame_black, x, y, text, FONT_SMILEY24, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)
        self._display.draw_image(self.frame_black, x + text_width, y, symbol, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)

    def draw_daily_weather(self, weather, x):
        x = LEFT + x * (ICON_SIZE + ICON_SPACING)

        # draw frame
        self._display.draw_image(self.frame_black, x, ICON_TOP, IMG_WEATHER_FRAME, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)

        # draw condition icon
        is_day = is_day_light(time.localtime()[3])
        condition = parse_weather_condition_id(weather['weather'][is_day])
        icon = self.get_weather_condition_icon(condition, is_day)
        if icon:
            self._display.draw_image(self.frame_black, x + 2, ICON_TOP + 21, icon, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)
        
        # draw day
        self._display.draw_text(self.frame_black, x + 5, ICON_TOP, I18N_DAYS_ABBREVIATIONS[time.localtime()[6]], DisplayEPD7in5.WHITE, DisplayEPD7in5.TOP_LEFT)
        self._display.draw_text(self.frame_black, x + 64 -5, ICON_TOP, b'{}'.format(weather['date'].split('-')[-1]), DisplayEPD7in5.WHITE, DisplayEPD7in5.TOP_LEFT)

        # draw high temp
        self.draw_weather_info_text(b'{}'.format(weather['temperature'][1]), IMG_WEATHER_INFO_DEGREE_SYMBOL, x + 32, ICON_TOP + 83)

        # draw low temp
        self.draw_weather_info_text(b'{}'.format(weather['temperature'][0]), IMG_WEATHER_INFO_DEGREE_SYMBOL, x + 32, ICON_TOP + 108)

    def draw_lunar_info(self):
        pass 

    def draw_birthday_info(self):
        pass