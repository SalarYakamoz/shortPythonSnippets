
from PIL import Image
import os, sys

path = "C:/Users/srazavi/PycharmProjects/mitosisCrop/upsamledMitosis/images/"
dirs = os.listdir(path)


for item in dirs:
    if os.path.isfile(path + item):
        im = Image.open(path + item)
        f, e = os.path.splitext(path + item)
        imResize = im.resize((256, 256), Image.ANTIALIAS)
        imResize.convert('RGB').save(f+'.png', 'png', quality=80)

