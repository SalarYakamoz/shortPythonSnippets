import os, sys
import cv2
import numpy as np

path = "G:/GAN_project/distance_metrics/real_images/"
dirs = os.listdir(path)


for item in dirs:
    if os.path.isfile(path + item):
        img = cv2.imread(path + item)
        img = cv2.resize(img, (1024, 1024))
        cv2.imwrite(item[:-3] + 'jpg', img)