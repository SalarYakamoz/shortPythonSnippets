import os
import glob
import csv
from PIL import Image

# Enter Directory of each directory manually
img_dir = "C:/Users/srazavi/PycharmProjects/mitosisCrop/cropped/"
data_path = os.path.join(img_dir, '*')
files = glob.glob(data_path)
data = []
iteration = 0
new_width = new_height = 50

for file in files:
    image = Image.open(file)
    width, height = image.size  # Get dimensions
    left = (width - new_width) / 2
    top = (height - new_height) / 2
    right = (width + new_width) / 2
    bottom = (height + new_height) / 2
    data.append(image)
    # Crop the center of the image
    image = image.crop((left, top, right, bottom))
    image.save("C:/Users/srazavi/PycharmProjects/mitosisCrop/resizedMitosis/" + str(iteration) + "mitosis.png")
    iteration = iteration + 1