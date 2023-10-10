# ****************************** build fonts ******************************
python build_font.py ./SmileySans-Oblique.ttf -name smiley32 -size 32 -ranges 月,日,星,期,周,正,腊,冬,寒,一,二,三,四,五,六,七,八,九,十,初,宜,忌,甲,乙,丙,丁,戊,己,庚,辛,壬,癸,子,丑,寅,卯,辰,巳,午,未,申,酉,戌,亥,鼠,牛,虎,兔,龙,蛇,马,羊,猴,鸡,狗,猪,(,),（,） -fg=0 -bg=255
python build_font.py ./SmileySans-Oblique.ttf -name smiley320 -size 320 -ranges 1,2,3,4,5,6,7 -fg=0 -bg=255

# ****************************** cropping zodiac image ******************************
python cut_zodiac.py ./

# ****************************** build image ******************************
# build image for chinese zodiac
python build_image.py rat.png ./
python build_image.py ow.png ./
python build_image.py tiger.png ./
python build_image.py rabbit.png ./
python build_image.py dragon.png ./
python build_image.py snake.png ./
python build_image.py horse.png ./
python build_image.py goat.png ./
python build_image.py monkey.png ./
python build_image.py rooster.png ./
python build_image.py dog.png ./
python build_image.py pig.png ./
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
