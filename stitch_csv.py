import os
import cv2
import glob
import numpy as np
import scipy.io as sio
import re
import pandas as pd
# dirname = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18',
#            '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36',
#            '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54',
#            '14', '15', '16', '17', '18',
#            '19', '20', '21']
pathOrg ='g:/mitosis_dataset/tupac16/mitoses_ground_truth/'
path = os.listdir(pathOrg)

for dirname in path: #patient name


    filepath_csv = pathOrg + dirname + '/*.csv'

    if int(dirname) < 24:
        img_folder = 'g:/mitosis_dataset/tupac16/center1/'
    elif 24 <= int(dirname) < 48:
        img_folder = 'g:/mitosis_dataset/tupac16/center2/'
    elif int(dirname) >= 48:
        img_folder = 'g:/mitosis_dataset/tupac16/center3/'

    img = glob.glob(filepath_csv) #getting HPFs for each patient
    n = len(img)
    for j in range(n): #HPF number
        imgname = img[j].split('/')[-1]

        dataCoord = pd.read_csv(pathOrg + imgname, header=None)

        locations = [(int(x[0]), int(x[1])) for x in dataCoord.values.tolist()]

        base = os.path.splitext(imgname)[0]
        newName = base + ".tif"
        filepath_img = img_folder + newName
        img_out = cv2.imread(filepath_img)
        for loc in locations:
            cv2.rectangle(img_out, (loc[1]-20, loc[0]-20), (loc[1]+20, loc[0]+20), (0, 255, 0), 2)

        img_out = cv2.imwrite(img_folder + base + "_mask.png", img_out)
        # stitchpatch(root_folder, dirname[i], imgname, featfolder, savefolder)
        # stitchpatchimg(root_folder, dirname[i], imgname, savefolder)
        #
