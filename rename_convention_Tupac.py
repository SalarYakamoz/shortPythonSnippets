import cv2
import os

allMaskPath ="E:\\camelyon16\\dataset_for_training\\level_1\\dataset\\more_than_70\\val_mask\\"
allPatches = "E:\\camelyon16\\dataset_for_training\\level_1\\dataset\\more_than_70\\val\\"
maskDst = "E:\\camelyon16\\dataset_for_training\\level_1\\dataset\\more_than_70\\val_mask_1\\"
tumorDst = "E:\\camelyon16\\dataset_for_training\\level_1\\dataset\\more_than_70\\test\\"
# tumorDst_1 = "E:\\camelyon16\\level_2\\n_t_mask_1\\"
allMaskPathdirs = os.listdir(allMaskPath)
allPatchesdirs = os.listdir(allPatches)
maskdstDir = os.listdir(maskDst)


def mask_division():
    # try:
    #     os.mkdir(maskDst+"/results")
    #     os.mkdir(maskDst+"/masks_1")
    # except OSError:
    #     print("Creation of the directory %s failed" % maskDst)
    # else:
    #     print("Successfully created the directory %s " % maskDst)
    for item in allMaskPathdirs:
        filenameMask, e = os.path.splitext(item)
        parts = filenameMask.split('_')
        image = cv2.imread(allMaskPath + filenameMask+".png",1)
        # if (tottaly_white(image) == False):
        #     image = image / 255
        # image = image * 255
        # cv2.imwrite(maskDst + parts[0]+"_"+parts[1]+"_"+parts[2]+"_"+parts[3]+".png", image)
        # cv2.imwrite(maskDst +"/masks_1"+ filenameMask+".png", image)
        cv2.imwrite(maskDst +filenameMask+".png", image)


# def copy_mask_with_same_tumor_name_2():
#     for item in allPatchesdirs:
#         filenameMask, e = os.path.splitext(item)
#         parts = filenameMask.split('_')
#         im = cv2.imread(allMaskPath + parts[0] + "_" + parts[1] + "_" + parts[2] + "_" + parts[3] + "_mask"+".png", 1)
#         # fileNameTumor, e1 = os.path.splitext(item2)
#         # im = Image.open(allMaskPath + filenameMask+"_mask.png")
#         cv2.imwrite(maskDst + parts[0] + "_" + parts[1] + "_" + parts[2] + "_" + parts[3] + ".png", im)
#         # im.save(maskDst + item)