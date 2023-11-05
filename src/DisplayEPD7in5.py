#!/usr/bin/env python
# -*- coding: utf-8 -*-
from machine import Pin
from time import sleep_ms

BLACK = 0
WHITE = 1
RED = WHITE

EPD_WIDTH       = 800
EPD_HEIGHT      = 480

ROTATION_0      = 0
ROTATION_90     = 1
ROTATION_180    = 2
ROTATION_270    = 3

_ALIGN_LEFT     = 0b000001
_ALIGN_TOP      = 0b000010
_ALIGN_RIGHT    = 0b000100
_ALIGN_BOTTOM   = 0b001000
_ALIGN_VCENTER  = 0b010000
_ALIGN_HCENTER  = 0b100000
TOP_LEFT        = _ALIGN_LEFT | _ALIGN_TOP
TOP_CENTER      = _ALIGN_TOP | _ALIGN_HCENTER
TOP_RIGHT       = _ALIGN_TOP | _ALIGN_RIGHT
RIGHT_CENTER    = _ALIGN_RIGHT | _ALIGN_VCENTER
BOTTOM_RIGHT    = _ALIGN_BOTTOM | _ALIGN_RIGHT
BOTTOM_CENTER   = _ALIGN_BOTTOM | _ALIGN_HCENTER
BOTTOM_LEFT     = _ALIGN_BOTTOM | _ALIGN_LEFT
LEFT_CENTER     = _ALIGN_LEFT | _ALIGN_VCENTER
CENTER          = _ALIGN_HCENTER | _ALIGN_VCENTER


class DisplayEPD7in5:
    def __init__(self, spi, cs, dc, rst, busy):
        self.spi = spi
        self.cs = Pin(cs, Pin.OUT, value=1)
        self.dc = Pin(dc, Pin.OUT, value=0)
        self.rst = Pin(rst, Pin.OUT, value = 0)
        self.busy = Pin(busy, Pin.IN)
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        self.rotation = ROTATION_0

        self.init()
    
    def init(self):
        self.reset()
        
        # self.send_command(0x06)   # btst
        # self.send_data(0x17)
        # self.send_data(0x17)
        # self.send_data(0x38)      # If an exception is displayed, try using 0x38
        # self.send_data(0x17)

        self.send_command(0x01)     # POWER SETTING
        self.send_data(0x07)
        self.send_data(0x07)        # VGH=20V,VGL=-20V
        self.send_data(0x3f)        # VDH=15V
        self.send_data(0x3f)        # VDL=-15V

        self.send_command(0x04)     # POWER ON
        sleep_ms(100)
        self.read_busy()

        self.send_command(0X00)     # PANNEL SETTING
        self.send_data(0x0F)        # KW-3f KWR-2F BWROTP-0f BWOTP-1f

        self.send_command(0x61)     # tres
        self.send_data(0x03)        # source 800
        self.send_data(0x20)
        self.send_data(0x01)        # gate 480
        self.send_data(0xE0)

        self.send_command(0X15)
        self.send_data(0x00)

        self.send_command(0X50)     # VCOM AND DATA INTERVAL SETTING
        self.send_data(0x11)
        self.send_data(0x07)

        self.send_command(0X60)     # TCON SETTING
        self.send_data(0x22)

        self.send_command(0x65)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
    
        return 0

    """
        basic drive functions
    """
    def send_data(self, data):
        self.dc.value(1)
        self.cs.value(0)
        self.spi.write(data.to_bytes(1,'big'))
        self.cs.value(1) 

    def send_command(self, command):
        self.dc.value(0)
        self.cs.value(0)
        self.spi.write(command.to_bytes(1,'big'))
        self.cs.value(1)
    
    def read_busy(self):
        #  0: idle, 1: busy
        while self.busy == 1:
            sleep_ms(10)
    
    def clear(self):
        self.send_command(0x10)  # DTM1
        for i in range(0, self.width/8*self.height):
            self.send_data(0xff)
        
        self.send_command(0x13)  # DTM2
        for i in range(0, self.width/8*self.height):
            self.send_data(0x00)
                
        self.send_command(0x12)
        sleep_ms(100)
        self.read_busy()
        
    def clear_frame(self, frame_buffer_black, frame_buffer_red=None):
        for i in range(int(self.width * self.height / 8)):
            frame_buffer_black[i] = 0xFF
            if frame_buffer_red is not None:
                frame_buffer_red[i] = 0x00

    def sleep(self):
        self.send_command(0x02)  # POWER_OFF
        self.read_busy()
        
        self.send_command(0x07)  # DEEP_SLEEP
        self.send_data(0XA5)

        sleep_ms(2000)

    def reset(self):
        self.rst.value(1) 
        sleep_ms(20) 
        self.rst.value(0)
        sleep_ms(5)
        self.rst.value(1)
        sleep_ms(20) 
    
    def set_rotation(self, rotation):
        self.rotation = rotation
        if rotation == ROTATION_0 or rotation == ROTATION_180:
            self.width = EPD_WIDTH
            self.height = EPD_HEIGHT
        else:
            self.width = EPD_HEIGHT
            self.height = EPD_WIDTH

    def set_pixel(self, frame_buffer, x, y, color):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return
        if self.rotation == ROTATION_0:
            self.set_absolute_pixel(frame_buffer, x, y, color)
        elif self.rotation == ROTATION_90:
            t = x
            x = EPD_WIDTH - y
            y = t
            self.set_absolute_pixel(frame_buffer, x, y, color)
        elif self.rotation == ROTATION_180:
            x = EPD_WIDTH - x
            y = EPD_HEIGHT- y
            self.set_absolute_pixel(frame_buffer, x, y, color)
        elif self.rotation == ROTATION_270:
            t = x
            x = y
            y = EPD_HEIGHT - t
            self.set_absolute_pixel(frame_buffer, x, y, color)
    
    def set_absolute_pixel(self, frame_buffer, x, y, color):
        # To avoid display orientation effects
        # use EPD_WIDTH instead of self.width
        # use EPD_HEIGHT instead of self.height
        if (x < 0 or x >= EPD_WIDTH or y < 0 or y >= EPD_HEIGHT):
            return
        if color:  
            frame_buffer[(x + y * EPD_WIDTH) // 8] |= 0x80 >> (x % 8)  # white == 1
        else:
            frame_buffer[(x + y * EPD_WIDTH) // 8] &= ~(0x80 >> (x % 8))  # black == 0
    
    def _align(self, x, y, width, height, align):
        if align & _ALIGN_HCENTER:
            x -= width // 2
        elif align & _ALIGN_RIGHT:
            x -= width 
        
        if align & _ALIGN_VCENTER:
            y -= height // 2
        elif align & _ALIGN_BOTTOM:
            y -= height
        return x, y

    def display(self, black_image=None, red_image=None):
        if black_image != None:
            self.send_command(0x10)
            sleep_ms(2)
            for i in range(0, self.width * self.height // 8):
                self.send_data(black_image[i])
            sleep_ms(2)
            
            self.send_command(0x92)  # Partial Out (PTOUT)
            
        if red_image != None:
            self.send_command(0x13)
            sleep_ms(2)
            for i in range(0, self.width * self.height // 8):
                self.send_data(red_image[i])
            sleep_ms(2)

        self.send_command(0x12)
        sleep_ms(100)
        self.read_busy()
    
    """
        drawing functions
    """
    def draw_hline(self, frame_buffer, x, y, length, thickness, color, align):
        x, y = self._align(x, y, length, thickness, align)
        for j in range(y, y + thickness):
            for i in range(x, x + length):
                self.set_pixel(frame_buffer, i, j, color) 
    
    def draw_vline(self, frame_buffer, x, y, length, thickness, color, align):
        x, y = self._align(x, y, thickness, length, align)
        for j in range(y, y + length):
            for i in range(x, x + thickness):
                self.set_pixel(frame_buffer, i, j, color)

    def draw_image(self, frame_buffer, x, y, image, align):
        self._align(x, y, image.width, image.height, align) 
        for j in range(0, image.height):
            for i in range(0, image.width):
                color = image[i][j]
                self.set_pixel(frame_buffer, x+i, y+j, color)
    
    def draw_text(self, line, font, x, y, align):
        pass 
    
    def draw_multiline_text(self, lines, font, x, y, align):
        pass 



