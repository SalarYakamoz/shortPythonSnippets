# SaLaR @ 01NOV2019
# to use the code three values in foldername, img_dir,
# foldername and value for mitosis numbers, and id name to write
# must be changed for each folder in TUPAC16 dataset

import os
import glob
import csv
from PIL import Image

# csv file name
id = 1
# change manually for each folder from 01 to 37
folderName = "G:/Mitosis dataset/Tupac16/new/label/73/"
filename = folderName + str(id) + ".csv"

# initializing the titles and rows list
rows = []

# reading csv file
with open(filename, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)

    # extracting each data row one by one
    for row in csvreader:
        rows.append(row)
        # get total number of rows
    print("Total no. of mitosis: %d" % (csvreader.line_num))

# Enter Directory of each directory manually
img_dir = "C:/Users/srazavi/PycharmProjects/mitosisCrop/image/73/"
data_path = os.path.join(img_dir, '*')
files = glob.glob(data_path)
data = []
iteration = 0
for file in files:
    image = Image.open(file)
    data.append(image)
    print('\n rows are:\n')
    for row in rows[:]:
        xCord = int(row[1])
        yCord = int(row[0])
        # left, top, right, bottom
        img2 = image.crop((xCord - 50, yCord - 50, xCord + 50, yCord + 50))
        # img2.show()
        img2.save("C:/Users/srazavi/PycharmProjects/mitosisCrop/cropped/" + str(iteration) + "mitosis.png")
        print("xCord: %10s" % xCord, "yCord: %10s" % yCord)
        print('\n')
        iteration = iteration + 1 + 4300 # value to make mitosis names be correct

    id = id + 1
    folderName = "G:/Mitosis dataset/Tupac16/new/label/73/"
    filename = folderName + str(id) + ".csv"

    # initializing the titles and rows list
    rows = []
    with open(filename, 'r') as csvfile:
         # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)







#  printing Mitosis coordinations
