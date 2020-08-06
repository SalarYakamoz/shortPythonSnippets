

from PIL import Image
import os, sys
import cv2
path = "C:/Users/srazavi/PycharmProjects/mitosisCrop/SRGAN/imagessuperresolution/mitosisNotUpsampled/images/"
dirs = os.listdir(path)


for item in dirs:
    if os.path.isfile(path + item):
        im = cv2.imread(path + item)
        f, e = os.path.splitext(path + item)
        paddedImage = cv2.copyMakeBorder(im, 103, 103, 103, 103, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        cv2.imwrite(f + '.png', paddedImage)
