#!/usr/bin/env python
# -*- coding: utf-8 -*-
import utime as time
from machine import SPI, Pin

from src import DisplayEPD7in5

from src.config import DIN_PIN, CLK_PIN, CS_PIN, DC_PIN, RESET_PIN, BUSY_PIN
from src.time_utils import get_days_in_month, is_day_light
from src.I18N import I18N_MONTHS, I18N_DAYS, I18N_DAYS_ABBREVIATIONS
from src.apis import get_weather_id, get_weather, get_lunar, parse_weather_condition_id

from resources.smiley16 import FONT_SMILEY16
from resources.smiley24 import FONT_SMILEY24
from resources.smiley32 import FONT_SMILEY32
from resources.smiley256 import FONT_SMILEY256

from resources.weather_frame import IMG_WEATHER_FRAME
from resources.weather_frame_empty import IMG_WEATHER_FRAME_EMPTY
from resources.weather_cloudy import IMG_WEATHER_CLOUDY
from resources.weather_day_clear import IMG_WEATHER_DAY_CLEAR
from resources.weather_night_clear import IMG_WEATHER_NIGHT_CLEAR
from resources.weather_partly_cloudy_day import IMG_WEATHER_PARTLY_CLOUDY_DAY
from resources.weather_partly_cloudy_night import IMG_WEATHER_PARTLY_CLOUDY_NIGHT
from resources.weather_scattered_showers_day import IMG_WEATHER_SCATTERED_SHOWERS_DAY
from resources.weather_scattered_showers_night import IMG_WEATHER_SCATTERED_SHOWERS_NIGHT
from resources.weather_showers import IMG_WEATHER_SHOWERS
from resources.weather_thunderstorms import IMG_WEATHER_THUNDERSTORMS
from resources.weather_fog import IMG_WEATHER_FOG
from resources.weather_snow import IMG_WEATHER_SNOW
from resources.weather_info_degree_symbol import IMG_WEATHER_INFO_DEGREE_SYMBOL
from resources.weather_info_percent_symbol import IMG_WEATHER_INFO_PERCENT_SYMBOL
from resources.error import IMG_ERROR


H_CENTER = 225
ICON_SIZE = 64
ICON_SPACING = 9
LEFT =  82
RIGHT = LEFT + ICON_SIZE * 5 + ICON_SPACING * 4
WIDTH = RIGHT - LEFT
ICON_TOP = 550


class Display:
    def __init__(self):
        fb_size = int(DisplayEPD7in5.EPD_WIDTH * DisplayEPD7in5.EPD_HEIGHT / 8)
        self.frame_black = bytearray(fb_size)
        self.frame_red = bytearray(fb_size)
    
    def init(self):
        # self._display = DisplayEPD7in5.DisplayEPD7in5(spi, cs=10, dc=13, rst=1, busy=3)
        spi = SPI(1, 115200, sck=Pin(CLK_PIN), mosi=Pin(DIN_PIN))
        self._display = DisplayEPD7in5.DisplayEPD7in5(spi, cs=CS_PIN, dc=DC_PIN, rst=RESET_PIN, busy=BUSY_PIN)
        self._display.set_rotation(DisplayEPD7in5.ROTATION_270)

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

    def update(self, date_fmt):
        self.init()

        year, month, day, hour, minute, second, weekday, yearday = time.localtime()
        days_in_month = get_days_in_month(month, year)

        # static lines
        self._display.draw_hline(self.frame_black, LEFT, 50, WIDTH, 2, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)
        self._display.draw_hline(self.frame_black, LEFT, 430, WIDTH, 2, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)
        self._display.draw_hline(self.frame_black, LEFT, 538, WIDTH, 2, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)

        # family logo

        # show BIG Date
        line = b'{}'.format(day)
        self._display.draw_text(self.frame_black, LEFT, 16, line, FONT_SMILEY256, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT, 10)

        # show small date
        # line = b'{}/{}'.format(month, day)
        # self._display.draw_text(self.frame_black, line, LEFT, 394, FONT_SMILEY32, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)

        # show day name
        self._display.draw_text(self.frame_black, RIGHT, 394, I18N_DAYS[weekday], FONT_SMILEY32, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_RIGHT)
        # show month name
        self._display.draw_text(self.frame_black, LEFT, 14, I18N_MONTHS[month-1], FONT_SMILEY32, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)
        # show year
        self._display.draw_text(self.frame_black, RIGHT, 14, b'{}'.format(year), FONT_SMILEY32, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_RIGHT)
        
        # show lunar info
        # show birthday info
        lunar_res = get_lunar(date_fmt)
        self.draw_birthday_info(lunar_res.pop('birth_coming'))
        self.draw_zodiac_pic(lunar_res.pop('zodiac_no'))
        self.draw_lunar_info(lunar_res)
        
        # show weather
        wids = get_weather_id()
        weathers = get_weather(wids)
        i = 0
        for weather in weathers['future']:
            self.draw_daily_weather(weather, i)
            i += 1
            
        self._display.display(self.frame_black, self.frame_red)
        self._display.sleep()
    
    def draw_zodiac_pic(self, no):
        black_image, red_image = self.get_zodiac_pic(no)
        self._display.draw_image(self.frame_black, 240, 100, black_image, DisplayEPD7in5.BLACK, DisplayEPD7in5.NONE_ALIGN)
        self._display.draw_image(self.frame_black, 240, 100, red_image, DisplayEPD7in5.RED, DisplayEPD7in5.NONE_ALIGN)
    
    def get_zodiac_pic(self, no):
        if no == 0:
            from resources.res_rat_black import IMG_RES_RAT_BLACK
            from resources.res_rat_red import IMG_RES_RAT_RED
            return IMG_RES_RAT_BLACK, IMG_RES_RAT_RED
        elif no == 1:
            from resources.res_ow_black import IMG_RES_OW_BLACK
            from resources.res_ow_red import IMG_RES_OW_RED
            return IMG_RES_OW_BLACK, IMG_RES_OW_RED
        elif no == 2:
            from resources.res_tiger_black import IMG_RES_TIGER_BLACK
            from resources.res_tiger_red import IMG_RES_TIGER_RED
            return IMG_RES_TIGER_BLACK, IMG_RES_TIGER_RED
        elif no == 3:
            from resources.res_rabbit_black import IMG_RES_RABBIT_BLACK
            from resources.res_rabbit_red import IMG_RES_RABBIT_RED
            return IMG_RES_RABBIT_BLACK, IMG_RES_RABBIT_RED
        elif no == 4:
            from resources.res_dragon_black import IMG_RES_DRAGON_BLACK
            from resources.res_dragon_red import IMG_RES_DRAGON_RED
            return IMG_RES_DRAGON_BLACK, IMG_RES_DRAGON_RED
        elif no == 5:
            from resources.res_snake_black import IMG_RES_SNAKE_BLACK
            from resources.res_snake_red import IMG_RES_SNAKE_RED
            return IMG_RES_SNAKE_BLACK, IMG_RES_SNAKE_RED
        elif no == 6:
            from resources.res_horse_black import IMG_RES_HORSE_BLACK
            from resources.res_horse_red import IMG_RES_HORSE_RED
            return IMG_RES_HORSE_BLACK, IMG_RES_HORSE_RED
        elif no == 7:
            from resources.res_goat_black import IMG_RES_GOAT_BLACK
            from resources.res_goat_red import IMG_RES_GOAT_RED
            return IMG_RES_GOAT_BLACK, IMG_RES_GOAT_RED
        elif no == 8:
            from resources.res_monkey_black import IMG_RES_MONKEY_BLACK
            from resources.res_monkey_red import IMG_RES_MONKEY_RED
            return IMG_RES_MONKEY_BLACK, IMG_RES_MONKEY_RED
        elif no == 9:
            from resources.res_rooster_black import IMG_RES_ROOSTER_BLACK
            from resources.res_rooster_red import IMG_RES_ROOSTER_RED
            return IMG_RES_ROOSTER_BLACK, IMG_RES_ROOSTER_RED
        elif no == 10:
            from resources.res_dog_black import IMG_RES_DOG_BLACK
            from resources.res_dog_red import IMG_RES_DOG_RED
            return IMG_RES_DOG_BLACK, IMG_RES_DOG_RED
        elif no == 11:
            from resources.res_pig_black import IMG_RES_PIG_BLACK
            from resources.res_pig_red import IMG_RES_PIG_RED
            return IMG_RES_PIG_BLACK, IMG_RES_PIG_RED
        else:
            return None 

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
        self._display.draw_text(self.frame_black, x + 5, ICON_TOP, I18N_DAYS_ABBREVIATIONS[(time.localtime()[6]+x)%7], FONT_SMILEY16, DisplayEPD7in5.WHITE, DisplayEPD7in5.TOP_LEFT)
        self._display.draw_text(self.frame_black, x + 64 -5, ICON_TOP, b'{}'.format(weather['date'].split('-')[-1]), FONT_SMILEY16, DisplayEPD7in5.WHITE, DisplayEPD7in5.TOP_LEFT)

        # draw high temp
        self.draw_weather_info_text(b'{}'.format(weather['temperature'][1]), IMG_WEATHER_INFO_DEGREE_SYMBOL, x + 32, ICON_TOP + 83)

        # draw low temp
        self.draw_weather_info_text(b'{}'.format(weather['temperature'][0]), IMG_WEATHER_INFO_DEGREE_SYMBOL, x + 32, ICON_TOP + 108)

    def draw_lunar_info(self, lunar_info):
        line = b'{}{}'.format(lunar_info['lunar_year'], lunar_info['lunar'])
        self._display.draw_text(self.frame_black, LEFT, 394, line, FONT_SMILEY32, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)
        self._display.draw_filled_circle(self.frame_black, LEFT, 480, 16, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)
        self._display.draw_text(self.frame_black, LEFT, 465, b'忌', FONT_SMILEY24, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)
        self._display.draw_text(self.frame_black, LEFT, 420, lunar_info['suit'].encode('utf8'), FONT_SMILEY24, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)
        self._display.draw_text(self.frame_black, LEFT, 465, lunar_info['avoid'].encode('utf8'), FONT_SMILEY24, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)
        
        self._display.draw_filled_circle(self.frame_red, LEFT, 420, 18, DisplayEPD7in5.RED, DisplayEPD7in5.TOP_LEFT)
        self._display.draw_text(self.frame_red, LEFT, 405, b'宜', FONT_SMILEY24, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)

    def draw_birthday_info(self, birth_list):
        i, x, y = 0, 10, 400
        if len(birth_list) > 0:
            for birth in birth_list:
                name = list(birth.items())[0][0]
                dt, err = list(birth.items())[0][1]
                print('{}还有{}天生日：{}'.format(name, err, dt))
                line = b'{}还有{}天生日：{}'.format(name, err, dt)
                self._display.draw_text(self.frame_black, x, y + i*24, line, FONT_SMILEY24, DisplayEPD7in5.BLACK, DisplayEPD7in5.NONE_ALIGN)
                i += 1
