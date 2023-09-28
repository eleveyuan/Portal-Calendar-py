# Portal Calendar

[ZH](./README.md) | EN

## Movtivation
here is e-paper project motivated by [wuspy/portal_calendar](https://github.com/wuspy/portal_calendar)

when I saw this project, I found it is suitable for chinese lunar calendar. In my family, we still check lunar calendar for family members' birthday or travel plan.

![](img/lunar.jpg)


## Directory structure
- **frame** stl files for 3D print
- **img** images for readme
- **resources** static files, eg. fonts, images
- **src** source code

## Materials
**Notification**: if you use amazone, just check the list in [wuspy/portal_calendar](https://github.com/wuspy/portal_calendar). this list is for guys who use Taobao(淘宝)

- **Waveshare 7.5" 800x480 E-Ink display** avaliable from [waveshare](https://www.waveshare.net/left_column/e-Paper.htm) or from [taobao](https://detail.tmall.com/item.htm?id=633262461077)
![](img/display-zh.png)

- **EzSBC ESP32 breakout board** esp32 can also be bought from taobao, just search it (BTW. it's very cheap, like it)
- **4xAAA battery holder** search it on taobao(AAA battery is an American dry battery standard, and the No.7 battery standard is compatible with it)
- **9x M3x8 cap head screws** same. taobao it
- **frame** print it through 3D printer, or taobao it and send stl file to the online store. here is outlook of my frame
![](img/frame.png)

## Implementation
In truth, I'm not good at C/C++. With the development of programme. I can use [MicroPython](https://micropython.org/) solve my problem.  

Actually, in this project, it's not a computationally intensive projects. Micropython can handle it.

But the big problem is no enough docs. sometime we should read some source code.

### Micropython
1. Waveshare does not provide a micropython driver. but we learn and rewrite the python driver code in [waveshare repositore](https://github.com/waveshareteam/e-Paper/tree/master/RaspberryPi_JetsonNano/python)
2. If we want to support Timezone, we'd better check the code writen by [mPython board](https://github.com/labplus-cn). Micropython's [ntptime](https://github.com/micropython/micropython-lib/blob/master/micropython/net/ntptime/ntptime.py) module doee not implement this function.
3. In this project, we must query some requests for network resource(API). Micropython provide a [urequests](https://makeblock-micropython-api.readthedocs.io/en/latest/public_library/Third-party-libraries/urequests.html) module can work for it, but it is not as good as Requests


