import os, sys
import cv2
allcenter = "G:/Mitosis_dataset/renamed_tupac16/centers/"
maskDst = "G:/Mitosis_dataset/renamed_tupac16/masks/"
imgDst = 'G:/Mitosis_dataset/renamed_tupac16/imgs/'
# tumorDst_1 = "E:\\camelyon16\\level_2\\n_t_mask_1\\"
all_center_dirs = os.listdir(allcenter)
maskdstDir = os.listdir(maskDst)
def naming_convenion():
    for item in all_center_dirs:
        center_name, e = os.path.splitext(item)
        patient_folder = allcenter + center_name + "/"
        patient_folder_dir = os.listdir(patient_folder)
        for item2 in patient_folder_dir:
            patient_name, e = os.path.splitext(item2)
            HPFz = patient_folder + item2 + "/"
            HPFz_dir = os.listdir(HPFz)
            for item3 in HPFz_dir:

                HPFz_name, e = os.path.splitext(item3)
                if e == ".tif":
                    image = cv2.imread(HPFz+HPFz_name + ".tif", 1)
                    cv2.imwrite(
                        imgDst + "Tupac_ROI_Training_" + center_name + "_patient" + patient_name + "_HPF" + HPFz_name + ".tif",
                        image)
                elif e == ".png":

                    if os.path.isfile(HPFz + HPFz_name + ".png"):
                        image_mask = cv2.imread(HPFz + HPFz_name + ".png", 1)
                        cv2.imwrite(
                            maskDst + "Tupac_ROI_Training_" + center_name + "_patient" + patient_name + "_HPF" + HPFz_name +".png",
                            image_mask)



if __name__ == '__main__':
    # resize()
    naming_convenion()