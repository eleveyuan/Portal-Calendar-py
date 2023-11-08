import os
import argparse
import subprocess

import cv2
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("path", type=str, help="image to be separated")
parser.add_argument("-dir", type=str, required=False, default='./', help="dir of result images to be saved")
args = parser.parse_args()

path_ = args.path
result_name = os.path.split(path_)[-1].split('.')[0]

current_path = os.getcwd()

img = cv2.imread(path_)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
colors = np.where(hist > 5000)
img_number = 0
platte = ['black', 'red']

for color in colors[0]:
    print(color)
    split_image = img.copy()
    split_image[np.where(gray != color)] = 255
    cv2.imwrite(result_name + '_' + platte[img_number]+".bmp", split_image)
    img_number += 1
