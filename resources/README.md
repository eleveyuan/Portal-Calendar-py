## Description

This readme descripe some functions for each python file.

**if you don't want to waste time for reading this readme, just run shell file(build_all.sh)**


### Picture cropping and splitting
Zodiac picutre(zodiac.png) is download from [图精灵/616pic](https://616pic.com/sucai/14nixpq7z.html), and it's only for this project, **not for commercial use**. 
Get BMP of each chinese zodiac for this pic, run this command line:
``` shell
python cut_zodiac.py ./
```

after cropping picture, we have to split picutre into two parts(red parts and black part). specifically, see this process in [issue #2](https://github.com/eleveyuan/Portal-Calendar-py/issues/2)
``` shell
magick xc:red xc:white xc:black +append palette.gif
magick rat.png -remap palette.gif res_rat.png
python split_image.py res_rat.png
```

### build fonts

There is two way to generate Glyphs I ever tried

**1.** use software which can generate Glyphs

![](../img/software.png)

**2.** or use python code provided by [wuspy/portal_calendar](https://github.com/wuspy/portal_calendar) (resources/build_font.py), but i rewriten it for my need. 

[wuspy/portal_calendar](https://github.com/wuspy/portal_calendar#bill-of-materials) mentioned waveshare e-paper is intended only for 2-greay level. He make some hacks to support 4-grey level. But this can't suit for every e-paper. I use 1-bits mode(0 for black, 1 for white) in this project.

> This display is intended only for 2-color greyscale (full black or full white, with no grey levels). However, this code does some hacks to it to make it support 4-color greyscale 
> for better antialiasing. I didn't invent this technique, the GxEPD2 project among others does the same thing. The downside of doing this, however, is that results can vary from 
> display to display. The greyscale levels may not look as good on your particular display as they do on mine. I've tried to design the graphics with that in mind so that the grey 
> level isn't critical to get things to look good, but I've only tried this on two of these displays, and I can't guarantee yours will look perfect.

``` shell
python build_font.py ./SmileySans-Oblique.ttf -name smiley320 -size 320 -ranges 1,2,3,4,5,6,7 -fg=0 -bg=255
```

***3.** construct your own family members word list(eg. name, birth)

```
abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
你的姓氏我的名字
:：，。’‘“”''-
还有几天生日倒计时
姓氏...
名字...
```

For Chinese characters, refer to [Simplified-Chinese-Characters](https://github.com/jinghu-moon/Simplified-Chinese-Characters)

### build images

It's pretty simple for building image. When buiding pictures, I performed padding on pictures whose width is not a multiple of 8.

```
IMG_WEATHER_INFO_DEGREE_SYMBOL = {
   "data": [
        ....
    ],
   "width": 8,   # original size: 7
   "height": 28,
   "pad": 1
}

```
