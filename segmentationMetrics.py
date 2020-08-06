from sklearn.metrics import confusion_matrix
import numpy as np

# masks should be converted from RGB to semantic map


import cv2
import numpy as np
import os


#numberClasses = 4

def compute_iou(y_pred, y_true):
     # ytrue, ypred is a flatten vector
     y_pred = y_pred.flatten()
     y_true = y_true.flatten()
     current = confusion_matrix(y_true, y_pred, labels=None)
     #currentNormalized = current / current.sum(axis=1)
     # compute mean iou
     intersection = np.diag(current)
     ground_truth_set = current.sum(axis=1)
     predicted_set = current.sum(axis=0)
     union = ground_truth_set + predicted_set - intersection
     IoU = intersection / union.astype(np.float32)
     return np.mean(IoU), current


def computeiou(y_pred_batch, y_true_batch):
    return np.mean(np.asarray([pixelaccuracy(y_pred_batch[i], y_true_batch[i]) for i in range(len(y_true_batch))]))

#
# def pixelaccuracy(y_pred, y_true):
#     img_rows, img_cols = y_pred.shape
#     if img_rows == img_cols:
#         y_pred = np.argmax(np.reshape(y_pred, [numberClasses, img_rows, img_cols]), axis=0)
#         y_true = np.argmax(np.reshape(y_true, [numberClasses, img_rows, img_cols]), axis=0)
#         y_pred = y_pred * (y_true>0)
#     else:
#         print('check image dimensions')
#     return 1.0 * np.sum((y_pred == y_true)*(y_true > 0)) / np.sum(y_true > 0)
#

import numpy as np


def pixel_accuracy(eval_segm, gt_segm):
    '''
    sum_i(n_ii) / sum_i(t_i)
    '''

    check_size(eval_segm, gt_segm)

    cl, n_cl = extract_classes(gt_segm)
    eval_mask, gt_mask = extract_both_masks(eval_segm, gt_segm, cl, n_cl)

    sum_n_ii = 0
    sum_t_i = 0

    for i, c in enumerate(cl):
        curr_eval_mask = eval_mask[i, :, :]
        curr_gt_mask = gt_mask[i, :, :]

        sum_n_ii += np.sum(np.logical_and(curr_eval_mask, curr_gt_mask))
        sum_t_i += np.sum(curr_gt_mask)

    if (sum_t_i == 0):
        pixel_accuracy_ = 0
    else:
        pixel_accuracy_ = sum_n_ii / sum_t_i

    return pixel_accuracy_


def mean_accuracy(eval_segm, gt_segm):
    '''
    (1/n_cl) sum_i(n_ii/t_i)
    '''

    check_size(eval_segm, gt_segm)

    cl, n_cl = extract_classes(gt_segm)
    eval_mask, gt_mask = extract_both_masks(eval_segm, gt_segm, cl, n_cl)

    accuracy = list([0]) * n_cl

    for i, c in enumerate(cl):
        curr_eval_mask = eval_mask[i, :, :]
        curr_gt_mask = gt_mask[i, :, :]

        n_ii = np.sum(np.logical_and(curr_eval_mask, curr_gt_mask))
        t_i = np.sum(curr_gt_mask)

        if (t_i != 0):
            accuracy[i] = n_ii / t_i

    mean_accuracy_ = np.mean(accuracy)
    return mean_accuracy_


def mean_IU(eval_segm, gt_segm):
    '''
    (1/n_cl) * sum_i(n_ii / (t_i + sum_j(n_ji) - n_ii))
    '''

    check_size(eval_segm, gt_segm)

    cl, n_cl = union_classes(eval_segm, gt_segm)
    _, n_cl_gt = extract_classes(gt_segm)
    eval_mask, gt_mask = extract_both_masks(eval_segm, gt_segm, cl, n_cl)

    IU = list([0]) * n_cl

    for i, c in enumerate(cl):
        curr_eval_mask = eval_mask[i, :, :]
        curr_gt_mask = gt_mask[i, :, :]

        if (np.sum(curr_eval_mask) == 0) or (np.sum(curr_gt_mask) == 0):
            continue

        n_ii = np.sum(np.logical_and(curr_eval_mask, curr_gt_mask))
        t_i = np.sum(curr_gt_mask)
        n_ij = np.sum(curr_eval_mask)

        IU[i] = n_ii / (t_i + n_ij - n_ii)

    mean_IU_ = np.sum(IU) / n_cl_gt
    return mean_IU_


def frequency_weighted_IU(eval_segm, gt_segm):
    '''
    sum_k(t_k)^(-1) * sum_i((t_i*n_ii)/(t_i + sum_j(n_ji) - n_ii))
    '''

    check_size(eval_segm, gt_segm)

    cl, n_cl = union_classes(eval_segm, gt_segm)
    eval_mask, gt_mask = extract_both_masks(eval_segm, gt_segm, cl, n_cl)

    frequency_weighted_IU_ = list([0]) * n_cl

    for i, c in enumerate(cl):
        curr_eval_mask = eval_mask[i, :, :]
        curr_gt_mask = gt_mask[i, :, :]

        if (np.sum(curr_eval_mask) == 0) or (np.sum(curr_gt_mask) == 0):
            continue

        n_ii = np.sum(np.logical_and(curr_eval_mask, curr_gt_mask))
        t_i = np.sum(curr_gt_mask)
        n_ij = np.sum(curr_eval_mask)

        frequency_weighted_IU_[i] = (t_i * n_ii) / (t_i + n_ij - n_ii)

    sum_k_t_k = get_pixel_area(eval_segm)

    frequency_weighted_IU_ = np.sum(frequency_weighted_IU_) / sum_k_t_k
    return frequency_weighted_IU_


'''
Auxiliary functions used during evaluation.
'''


def get_pixel_area(segm):
    return segm.shape[0] * segm.shape[1]


def extract_both_masks(eval_segm, gt_segm, cl, n_cl):
    eval_mask = extract_masks(eval_segm, cl, n_cl)
    gt_mask = extract_masks(gt_segm, cl, n_cl)

    return eval_mask, gt_mask


def extract_classes(segm):
    cl = np.unique(segm)
    n_cl = len(cl)

    return cl, n_cl


def union_classes(eval_segm, gt_segm):
    eval_cl, _ = extract_classes(eval_segm)
    gt_cl, _ = extract_classes(gt_segm)

    cl = np.union1d(eval_cl, gt_cl)
    n_cl = len(cl)

    return cl, n_cl


def extract_masks(segm, cl, n_cl):
    h, w = segm_size(segm)
    masks = np.zeros((n_cl, h, w))

    for i, c in enumerate(cl):
        masks[i, :, :] = segm == c

    return masks


def segm_size(segm):
    try:
        height = segm.shape[0]
        width = segm.shape[1]
    except IndexError:
        raise

    return height, width

def check_size(eval_segm, gt_segm):
    h_e, w_e = segm_size(eval_segm)
    h_g, w_g = segm_size(gt_segm)

    if (h_e != h_g) or (w_e != w_g):
        raise EvalSegErr("DiffDim: Different dimensions of matrices!")

'''
Exceptions
'''
class EvalSegErr(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


import os
# from os import path
# cv2 package is installed using pip install opencv-python
import cv2
# current path is fetched
current_path = os.getcwd()
# folder is fetched where images are located dynamically
folderReal = os.path.join(current_path, 'real_images')
folderFake = os.path.join(current_path, 'fake_images')

    # loop us implemented to read the images one by one from the loop.
    # listdir return a list containing the names of the entries
    # in the directory.
itr = 0
arraysSinglPixel = []
arraysSinglIouOne = []
arraysSinglIouTwo = []
cmTotal = []
for filename in os.listdir(folderReal):
    imgReal = cv2.imread((os.path.join(folderReal, filename)), cv2.IMREAD_ANYDEPTH)
    imgFake = cv2.imread((os.path.join(folderFake, filename)), cv2.IMREAD_ANYDEPTH)

    #print('pixel accuracy: {}'.format(pixelaccuracy(imgReal, imgFake)))
    #print('pixel_accuracy another method: {}'.format(pixel_accuracy(imgReal, imgFake)))
    arraysSinglPixel.append(pixel_accuracy(imgReal, imgFake))
    #print('mean iou: {}'.format(computeiou(imgReal, imgFake)))
    #print('mean iou another method: {}'.format(compute_iou(imgReal, imgFake)))
    iou, cm = compute_iou(imgReal, imgFake)
    arraysSinglIouOne.append(iou)
    cmTotal.append(cm)
    arraysSinglIouTwo.append(mean_IU(imgReal, imgFake))
    #print('mean iou another another method: {}'.format(mean_IU(imgReal, imgFake)))
    itr += 1

print('pixel_accuracy Total: {}'.format(np.mean(arraysSinglPixel)))

print('SinglIouOneTotal Total method: {}'.format(np.mean(arraysSinglIouOne)))

print('SinglIouTwoTotal Total another method: {}'.format(np.mean(arraysSinglIouTwo)))

print('CM Total another method: {}'.format(np.mean(cmTotal, axis=0)))


# n_cl : number of classes included in ground truth segmentation
#
# n_ij : number of pixels of class i predicted to belong to class j
# t_i : total number of pixels of class i in ground truth segmentation