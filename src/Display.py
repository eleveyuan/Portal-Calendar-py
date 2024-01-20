#!/usr/bin/env python
# -*- coding: utf-8 -*-
import utime as time
from machine import SPI, Pin

from src import DisplayEPD7in5

from src.config import DIN_PIN, CLK_PIN, CS_PIN, DC_PIN, RESET_PIN, BUSY_PIN, CITY, DISTRICT
from src.time_utils import get_days_in_month, is_day_light
from src.I18N import I18N_MONTHS, I18N_DAYS, I18N_DAYS_ABBREVIATIONS
from src.apis import get_weather_id, get_weather, get_lunar, parse_weather_condition_id

from resources.small16 import FONT_SMALL16
from resources.lunar24 import FONT_LUNAR24
from resources.birth24 import FONT_BIRTH24
from resources.middle32 import FONT_MIDDLE32
from resources.big256 import FONT_BIG256

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
from resources.local_icon import IMG_LOCAL_ICON


H_CENTER = 225
ICON_SIZE = 64
ICON_SPACING = 9
LEFT =  82
RIGHT = LEFT + ICON_SIZE * 5 + ICON_SPACING * 4
WIDTH = RIGHT - LEFT
ICON_TOP = 338
LUNAR_TOP = 500


class Display:
    def __init__(self):
        fb_size = int(DisplayEPD7in5.EPD_WIDTH * DisplayEPD7in5.EPD_HEIGHT / 8)
        self.frame_black = bytearray(fb_size)
        self.frame_red = bytearray(fb_size)
        self.lunar_height = 0
    
    def init(self):
        # self._display = DisplayEPD7in5.DisplayEPD7in5(spi, cs=10, dc=13, rst=1, busy=3)
        spi = SPI(1, 115200, sck=Pin(CLK_PIN), mosi=Pin(DIN_PIN))
        self._display = DisplayEPD7in5.DisplayEPD7in5(spi, cs=CS_PIN, dc=DC_PIN, rst=RESET_PIN, busy=BUSY_PIN)
        self._display.set_rotation(DisplayEPD7in5.ROTATION_270)
        self._display.clear_frame(self.frame_black, self.frame_red)

    def error(self, msg, will_retry):
        # show error message
        self.init()
        y = self._display.get_height() - self._display.get_height() / 1.618
        self._display.draw_image(self.frame_black, H_CENTER, y, IMG_ERROR, black, DisplayEPD7in5.BOTTOM_CENTER)
        self._display.draw_multiline_text(self.frame_black, H_CENTER, y + FONT_LUNAR24.ascent + FONT_LUNAR24.descent, msg, FONT_LUNAR24, black, DisplayGDEW075T7.TOP_CENTER)

        if will_retry:
            self._display.draw_multiline_text(self.frame_black, H_CENTER, self._display.get_height() - 12, [
            "Will try again in 1 hour. Or, press the RESET button",
            "on the back of the device to retry now."
            ], FONT_LUNAR24, black, DisplayGDEW075T7.BOTTOM_CENTER)
        
        self._display.display(self.frame_black)

    def update(self, date_fmt):
        self.init()

        year, month, day, hour, minute, second, weekday, yearday = time.localtime()
        days_in_month = get_days_in_month(month, year)

        # family logo

        # show BIG Date
        line = b'{:02}'.format(day)
        big_date_width = self._display.measure_text(line, FONT_BIG256)
        print(big_date_width)
        self._display.draw_text(self.frame_black, LEFT, 16, line, FONT_BIG256, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT, 10)

        # show day name
        self._display.draw_text(self.frame_black, RIGHT, 290, I18N_DAYS[weekday], FONT_MIDDLE32, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_RIGHT)
        # show month name
        self._display.draw_text(self.frame_black, LEFT, 14, I18N_MONTHS[month-1], FONT_MIDDLE32, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)
        # show year
        self._display.draw_text(self.frame_black, RIGHT, 14, b'{}'.format(year), FONT_MIDDLE32, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_RIGHT)
        
        # show lunar info
        # show birthday info
        lunar_res = get_lunar(date_fmt)
        birth_info = lunar_res.pop('birth_coming')
        self.draw_zodiac_pic(lunar_res.pop('zodiac_no'), big_date_width)
        self.draw_lunar_info(lunar_res)
        self.draw_birthday_info(birth_info)
        
        # show weather
        wids = get_weather_id()
        weathers = get_weather(wids)
        i = 0
        for weather in weathers['future']:
            self.draw_daily_weather(weather, i)
            i += 1
        
        # show locations
        self._display.draw_image(self.frame_black, 2, 620, IMG_LOCAL_ICON, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)
        line = [w.encode('utf8') for w in list("{}-{}".format(CITY, DISTRICT))]
        self._display.draw_multiline_text(self.frame_black, 10, 660, line, FONT_SMALL16, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)
        
        # static lines
        self._display.draw_hline(self.frame_black, LEFT, 50, WIDTH, 2, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)
        self._display.draw_hline(self.frame_black, LEFT, 326, WIDTH, 2, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)
        self._display.draw_hline(self.frame_black, LEFT, 488, WIDTH, 2, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)
        
        self._display.display(self.frame_black, self.frame_red)
        self._display.sleep()
    
    def draw_zodiac_pic(self, no, width):
        black_image, red_image = self.get_zodiac_pic(no)
        self._display.draw_image(self.frame_black, LEFT + width + 32, 16+50, black_image, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)
        self._display.draw_image(self.frame_red, LEFT + width + 32, 16+50, red_image, DisplayEPD7in5.RED, DisplayEPD7in5.TOP_LEFT)
    
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
        text_width = self._display.measure_text(text, FONT_SMALL16)
        x -= (text_width + symbol['width'] // 2) // 2
        self._display.set_alpha(DisplayEPD7in5.WHITE)
        self._display.draw_text(self.frame_black, x, y, text, FONT_SMALL16, DisplayEPD7in5.BLACK, DisplayEPD7in5.NONE_ALIGN)
        self._display.draw_image(self.frame_black, x + text_width, y-2, symbol, DisplayEPD7in5.BLACK, DisplayEPD7in5.NONE_ALIGN)
        self._display.set_alpha(DisplayEPD7in5.NO_ALPHA)

    def draw_daily_weather(self, weather, x):
        bias = x
        x = LEFT + x * (ICON_SIZE + ICON_SPACING)
        
        # draw frame
        self._display.draw_image(self.frame_black, x, ICON_TOP, IMG_WEATHER_FRAME, DisplayEPD7in5.BLACK, DisplayEPD7in5.NONE_ALIGN)
        
        # draw high temp
        self.draw_weather_info_text(b'{}'.format(weather['temperature'][1]), IMG_WEATHER_INFO_DEGREE_SYMBOL, x + 32, ICON_TOP + 90)
        # draw low temp
        self.draw_weather_info_text(b'{}'.format(weather['temperature'][0]), IMG_WEATHER_INFO_DEGREE_SYMBOL, x + 32, ICON_TOP + 111)

        # draw condition icon
        is_day = is_day_light(time.localtime()[3])
        condition = parse_weather_condition_id(weather['weather'][is_day])
        icon = self.get_weather_condition_icon(condition, is_day)
        if icon:
            self._display.set_alpha(DisplayEPD7in5.WHITE)
            self._display.draw_image(self.frame_black, x + 2, ICON_TOP + 21, icon, DisplayEPD7in5.BLACK, DisplayEPD7in5.NONE_ALIGN)
            self._display.set_alpha(DisplayEPD7in5.NO_ALPHA)
        
        # draw day
        self._display.set_alpha(DisplayEPD7in5.BLACK)
        self._display.draw_text(self.frame_black, x + 5, ICON_TOP + 2, I18N_DAYS_ABBREVIATIONS[(time.localtime()[6]+bias)%7], FONT_SMALL16, DisplayEPD7in5.WHITE, DisplayEPD7in5.NONE_ALIGN)
        self._display.draw_text(self.frame_black, x + 42, ICON_TOP + 2, b'{}'.format(weather['date'].split('-')[-1]), FONT_SMALL16, DisplayEPD7in5.WHITE, DisplayEPD7in5.NONE_ALIGN)
        self._display.set_alpha(DisplayEPD7in5.NO_ALPHA)

    def draw_lunar_info(self, lunar_info):
        line = b'{}{}'.format(lunar_info['lunar_year'], lunar_info['lunar'])
        self._display.draw_text(self.frame_black, LEFT, 290, line, FONT_MIDDLE32, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)
        if len(lunar_info['suit']) == 1:
            self._display.draw_text(self.frame_black, LEFT+36, LUNAR_TOP, lunar_info['suit'][0], FONT_LUNAR24, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)
        else:
            self._display.draw_multiline_text(self.frame_black, LEFT+36, LUNAR_TOP, lunar_info['suit'], FONT_LUNAR24, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)
        track = len(lunar_info['suit']) * 30 + 8
        self._display.draw_filled_circle(self.frame_black, LEFT+10, LUNAR_TOP+track+15, 18, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)
        self._display.draw_text(self.frame_black, LEFT, LUNAR_TOP+track, b'忌', FONT_LUNAR24, DisplayEPD7in5.WHITE, DisplayEPD7in5.TOP_LEFT)
        if len(lunar_info['avoid']) == 1:
            self._display.draw_text(self.frame_black, LEFT+36, LUNAR_TOP+track, lunar_info['avoid'][0], FONT_LUNAR24, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)
        else:
            self._display.draw_multiline_text(self.frame_black, LEFT+36, LUNAR_TOP+track, lunar_info['avoid'], FONT_LUNAR24, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)
        self.lunar_height = track + len(lunar_info['avoid']) * 30
        
        self._display.draw_filled_circle(self.frame_red, LEFT+10, LUNAR_TOP+15, 18, DisplayEPD7in5.RED, DisplayEPD7in5.TOP_LEFT)
        self._display.draw_text(self.frame_red, LEFT, LUNAR_TOP, b'宜', FONT_LUNAR24, DisplayEPD7in5.BLACK, DisplayEPD7in5.TOP_LEFT)

    def draw_birthday_info(self, birth_list):
        i, x = 0, LEFT
        y = LUNAR_TOP + self.lunar_height + 16 if self.lunar_height else LUNAR_TOP + 180
        if len(birth_list) > 0:
            for birth in birth_list:
                name = list(birth.items())[0][0]
                dt, err = list(birth.items())[0][1]
                print('{}还有{}天生日：{}'.format(name, err, dt))
                line = b'{}还有{}天生日：{}'.format(name, err, dt)
                self._display.draw_text(self.frame_black, x, y + i*24, line, FONT_BIRTH24, DisplayEPD7in5.BLACK, DisplayEPD7in5.NONE_ALIGN)
                i += 1

    def clear(self):
        self._display.clear()
