#Split the images in your dataset using image_slicer
import image_slicer
import glob

files = sorted(glob.glob('path to your images/*.png'))
count = 0
for image in files:
    tiles = image_slicer.slice(image, 4, False)
    image_slicer.save_tiles(tiles, directory='path to save the images',
                            prefix=str(count), format='png')
    count += 1
	
# ================================================================================================== #
#Augment your images and according masks for deep learning application. Here both original image and corresponding mask are augmented with a same function
import Augmentor
import numpy as np
from PIL import Image
import glob
from natsort import natsorted
import cv2


# Reading and sorting the image paths from the directories
ground_truth_images = natsorted(glob.glob("path to read images/*.png"))
segmentation_mask_images = natsorted(glob.glob("path to read masks/*.png"))

collated_images_and_masks = list(zip(ground_truth_images,
                                     segmentation_mask_images))

images = [[np.asarray(Image.open(y)) for y in x] for x in collated_images_and_masks]

p = Augmentor.DataPipeline(images)
p.rotate(1, max_left_rotation=5, max_right_rotation=5)
p.flip_top_bottom(1)
p.zoom_random(1, percentage_area=0.5)
p.flip_left_right(probability=0.5)
p.rotate90(probability=0.5)
# couldn't use contrast and histogram items as our masks are BW
# p.random_contrast(0.3, 0.5, 0.7)
# p.histogram_equalisation(0.3)
g = p.generator(batch_size=4000)
augmented_images = next(g)

for r_index in range(len(augmented_images)):
    cv2.imwrite("path to save images" + str(r_index) + ".png", augmented_images[r_index][0],   cv2.IMREAD_COLOR)
    cv2.imwrite("path to save masks/" + str(r_index) + "_mask.png", augmented_images[r_index][1],  cv2.IMREAD_COLOR)


