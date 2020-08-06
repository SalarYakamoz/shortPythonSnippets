import os, sys
import numpy as np
import cv2
from PIL import Image as pil_image

path = ""
dirs = os.listdir(path)

palette = [255, 255, 255, 
           0, 255, 0, 
           255, 255, 255,
           255, 0, 0,  
           0, 255, 255, 
           0, 0, 255, 
           255,255,255
           ]


def to_rgb(x):
    tdim = x.shape[0]
    a = np.zeros((tdim, tdim, 3), dtype='uint8')
    for i in range(tdim):
        for j in range(tdim):
            k = x[i, j]
            if k < 7:
                a[i, j, :] = palette[3 * k:3 * (k + 1)]
            else:
                a[i, j, :] = [255, 255, 255]
    return a

for item in dirs:
    if os.path.isfile(path + item):
        im = pil_image.open(path + item)
        im = im.resize([5120, 5120])
        y1 = to_rgb(np.array(im))
        f, e = os.path.splitext(path + item)
        print(f + ' :done')
        cv2.imwrite(f + 'new_color.png', y1)
