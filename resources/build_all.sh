# ****************************** build fonts ******************************
python build_font.py ./SmileySans-Oblique.ttf -name smiley32 -size 32 -ranges 月,日,星,期,周,正,腊,冬,寒,一,二,三,四,五,六,七,八,九,十,初,宜,忌,甲,乙,丙,丁,戊,己,庚,辛,壬,癸,子,丑,寅,卯,辰,巳,午,未,申,酉,戌,亥,鼠,牛,虎,兔,龙,蛇,马,羊,猴,鸡,狗,猪,(,),（,） -fg=0 -bg=255
python build_font.py ./SmileySans-Oblique.ttf -name smiley320 -size 320 -ranges 1,2,3,4,5,6,7 -fg=0 -bg=255

# ****************************** cropping zodiac image ******************************
python cut_zodiac.py ./

# ****************************** split image ******************************
magick xc:red xc:white xc:black +append palette.gif
magick rat.png -remap palette.gif res_rat.png
magick ow.png -remap palette.gif res_ow.png
magick tiger.png -remap palette.gif res_tiger.png
magick rabbit.png -remap palette.gif res_rabbit.png
magick dragon.png -remap palette.gif res_dragon.png
magick snake.png -remap palette.gif res_snake.png
magick horse.png -remap palette.gif res_horse.png
magick goat.png -remap palette.gif res_goat.png
magick monkey.png -remap palette.gif res_monkey.png
magick rooster.png -remap palette.gif res_rooster.png
magick dog.png -remap palette.gif res_dog.png
magick pig.png -remap palette.gif res_pig.png

python split_image.py res_rat.png ./
python split_image.py res_ow.png ./
python split_image.py res_tiger.png ./
python split_image.py res_rabbit.png ./
python split_image.py res_dragon.png ./
python split_image.py res_snake.png ./
python split_image.py res_horse.png ./
python split_image.py res_goat.png ./
python split_image.py res_monkey.png ./
python split_image.py res_rooster.png ./
python split_image.py res_dog.png ./
python split_image.py res_pig.png ./

# ****************************** build image ******************************
# build image for chinese zodiac
python build_image.py res_rat_black.bmp ./
python build_image.py res_ow_black.bmp ./
python build_image.py res_tiger_black.bmp ./
python build_image.py res_rabbit_black.bmp ./
python build_image.py res_dragon_black.bmp ./
python build_image.py res_snake_black.bmp ./
python build_image.py res_horse_black.bmp ./
python build_image.py res_goat_black.bmp ./
python build_image.py res_monkey_black.bmp ./
python build_image.py res_rooster_black.bmp ./
python build_image.py res_dog_black.bmp ./
python build_image.py res_pig_black.bmp ./

python build_image.py res_rat_red.bmp ./
python build_image.py res_ow_red.bmp ./
python build_image.py res_tiger_red.bmp ./
python build_image.py res_rabbit_red.bmp ./
python build_image.py res_dragon_red.bmp ./
python build_image.py res_snake_red.bmp ./
python build_image.py res_horse_red.bmp ./
python build_image.py res_goat_red.bmp ./
python build_image.py res_monkey_red.bmp ./
python build_image.py res_rooster_red.bmp ./
python build_image.py res_dog_red.bmp ./
python build_image.py res_pig_red.bmp ./

# build image for weather icon
python build_image.py weather_cloudy.gif ./
python build_image.py weather_day_clear.gif ./
python build_image.py weather_fog.gif ./
python build_image.py weather_frame.gif ./
python build_image.py weather_frame_empty.gif ./
python build_image.py weather_info_degree_symbol.gif ./
python build_image.py weather_info_percent_symbol.gif ./
python build_image.py weather_night_clear.gif ./
python build_image.py weather_partly_cloudy_day.gif ./
python build_image.py weather_partly_cloudy_night.gif ./
python build_image.py weather_scattered_showers_day.gif ./
python build_image.py weather_scattered_showers_night.gif ./
python build_image.py weather_showers.gif ./
python build_image.py weather_snow.gif ./
python build_image.py weather_thunderstorms.gif ./
