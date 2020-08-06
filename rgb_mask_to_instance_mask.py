from PIL import Image
import os
import numpy as np
import cv2

path = "G:/GAN_project/pix2pixHD/datasets/mitosis/train_label/"
dirs = os.listdir(path)
# bgr here but it is rgb in ImageJ
black = np.array([0, 0, 0])
green = np.array([0, 255, 0])
blue = np.array([255, 0, 0])
yellow = np.array([0, 255, 255])

for item in dirs:

    if os.path.isfile(path + item):
        image = cv2.imread(path + item)
        label_seg = np.zeros((image.shape[:2]), dtype=np.int)
        label_seg[(image == black).all(axis=2)] = 0
        label_seg[(image == green).all(axis=2)] = 1
        label_seg[(image == blue).all(axis=2)] = 2
        label_seg[(image == yellow).all(axis=2)] = 3
        cv2.imwrite(path + item, label_seg)
