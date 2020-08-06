from PIL import Image
import os, sys

path = ('G:/Gleason/Images/testRescale')

def resize():
    for item in os.listdir(path):
        if os.path.isfile(item):
            im = Image.open(item)
        f, e = os.path.splitext(item)
        imNew = im * 255
        imNew.save(f + 'resized.PNG', 'PNG', quality=90)

resize()