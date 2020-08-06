import os, sys
import numpy as np
import cv2
from PIL import Image as pil_image

path = "G:/Mitosis_dataset/renamed_tupac16/imgs/"
dirs = os.listdir(path)

size = (2000, 2000)
for item in dirs:
    if os.path.isfile(path + item):
        im = cv2.imread(path + item)
        #im = im.resize(size)
        #y1 = to_rgb(np.array(im))
        resized = cv2.resize(im, size, interpolation=cv2.INTER_AREA)
        f, e = os.path.splitext(path + item)
        print(f + ' :done')
        cv2.imwrite(f + '.tif', resized)
