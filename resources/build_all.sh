# ****************************** build fonts ******************************
python build_font.py ./ChillYunmoGothicCompactRegular.otf -name middle32 -size 32 -ranges 年,月,日,星,期,周,正,腊,冬,寒,一,二,三,四,五,六,七,八,九,十,廿,初,宜,忌,甲,乙,丙,丁,戊,己,庚,辛,壬,癸,子,丑,寅,卯,辰,巳,午,未,申,酉,戌,亥,鼠,牛,虎,兔,龙,蛇,马,羊,猴,鸡,狗,猪,(,),（,）,0,1,2,3,4,5,6,7,8,9,/ -fg=255 -bg=0
python build_font.py ./SmileySans-Oblique.ttf -name big256 -size 256 -ranges 0,1,2,3,4,5,6,7,8,9 -fg=255 -bg=0
python build_font.py ./ChillYunmoGothicCompactRegular.otf -name birth24 -size 24 -ranges birth  -fg=255 -bg=00
python build_font.py ./ChillYunmoGothicCompactRegular.otf -name lunar24 -size 24 -ranges lunar  -fg=255 -bg=00
python build_font.py ./LXGWWenKai-Light.ttf -name small16 -size 16 -ranges city -fg=255 -bg=00

# ****************************** cropping zodiac image ******************************
python cut_zodiac.py ./

# ****************************** split image ******************************
# remap all the colours to palette without dithering
magick xc:red xc:white xc:black +append palette.gif
magick rat.png +dither -remap palette.gif res_rat.png
magick ow.png +dither -remap palette.gif res_ow.png
magick tiger.png +dither -remap palette.gif res_tiger.png
magick rabbit.png +dither -remap palette.gif res_rabbit.png
magick dragon.png +dither -remap palette.gif res_dragon.png
magick snake.png +dither -remap palette.gif res_snake.png
magick horse.png +dither -remap palette.gif res_horse.png
magick goat.png +dither -remap palette.gif res_goat.png
magick monkey.png +dither -remap palette.gif res_monkey.png
magick rooster.png +dither -remap palette.gif res_rooster.png
magick dog.png +dither -remap palette.gif res_dog.png
magick pig.png +dither -remap palette.gif res_pig.png

python split_image.py res_rat.png -dir ./
python split_image.py res_ow.png -dir ./
python split_image.py res_tiger.png -dir ./
python split_image.py res_rabbit.png -dir ./
python split_image.py res_dragon.png -dir ./
python split_image.py res_snake.png -dir ./
python split_image.py res_horse.png -dir ./
python split_image.py res_goat.png -dir ./
python split_image.py res_monkey.png -dir ./
python split_image.py res_rooster.png -dir ./
python split_image.py res_dog.png -dir ./
python split_image.py res_pig.png -dir ./

# ****************************** build image ******************************
# build image for chinese zodiac
python build_image.py res_rat_black.bmp -dir ./
python build_image.py res_ow_black.bmp -dir ./
python build_image.py res_tiger_black.bmp -dir ./
python build_image.py res_rabbit_black.bmp -dir ./
python build_image.py res_dragon_black.bmp -dir ./
python build_image.py res_snake_black.bmp -dir ./
python build_image.py res_horse_black.bmp -dir ./
python build_image.py res_goat_black.bmp -dir ./
python build_image.py res_monkey_black.bmp -dir ./
python build_image.py res_rooster_black.bmp -dir ./
python build_image.py res_dog_black.bmp -dir ./
python build_image.py res_pig_black.bmp -dir ./

python build_image.py res_rat_red.bmp -dir ./
python build_image.py res_ow_red.bmp -dir ./
python build_image.py res_tiger_red.bmp -dir ./
python build_image.py res_rabbit_red.bmp -dir ./
python build_image.py res_dragon_red.bmp -dir ./
python build_image.py res_snake_red.bmp -dir ./
python build_image.py res_horse_red.bmp -dir ./
python build_image.py res_goat_red.bmp -dir ./
python build_image.py res_monkey_red.bmp -dir ./
python build_image.py res_rooster_red.bmp -dir ./
python build_image.py res_dog_red.bmp -dir ./
python build_image.py res_pig_red.bmp -dir ./

# build image for weather icon
python build_image.py weather_cloudy.gif -dir ./
python build_image.py weather_day_clear.gif -dir ./
python build_image.py weather_fog.gif -dir ./
python build_image.py weather_frame.gif -dir ./
python build_image.py weather_frame_empty.gif -dir ./
python build_image.py weather_info_degree_symbol.gif -dir ./
python build_image.py weather_info_percent_symbol.gif -dir ./
python build_image.py weather_night_clear.gif -dir ./
python build_image.py weather_partly_cloudy_day.gif -dir ./
python build_image.py weather_partly_cloudy_night.gif -dir ./
python build_image.py weather_scattered_showers_day.gif -dir ./
python build_image.py weather_scattered_showers_night.gif -dir ./
python build_image.py weather_showers.gif -dir ./
python build_image.py weather_snow.gif -dir ./
python build_image.py weather_thunderstorms.gif -dir ./
python build_image.py error.png -dir ./
python build_image.py local_icon.jpg -dir ./