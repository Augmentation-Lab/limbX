"""
1. Segment image into object regions.
2. Crop image to only include eye-tracked object without bg.
3. Use SIFT to map features from cropped image to target image.
4. Segment target image into object regions.
5. Select the object region containing the most mapped points.
"""

import cv2
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
import numpy as np
from skimage.filters import sobel
from skimage.feature import canny

# function that handles trackbar changes
def doClose(img, val):
    # create a kernel based on trackbar input
    kernel = np.ones((val,val))
    # do a morphologic close
    res = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    # save result
    return res

def process_input_img(imgPath):
    """
    Segment image into object regions.
    """
    image = cv2.imread(imgPath)
    imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # elevationMap = sobel(imgGray)
    # plt.imsave('elevationMap.png', elevationMap)
    # cv2.imwrite('imgGray.png', imgGray)

    edges_unfilled = canny(imgGray/255., sigma=1)
    plt.imsave('edges_unfilled.png', edges_unfilled)
    img = cv2.imread('edges_unfilled.png')
    edges = doClose(img, 5)
    # plt.imsave('edges.png', edges)
    newimg = cv2.cvtColor(edges, cv2.COLOR_BGR2GRAY)
    plt.imsave('newimg.png', newimg)
    filled = ndi.binary_fill_holes(newimg)
    plt.imsave('filled.png', filled)

process_input_img('mouse.png')
    

# #load image as grayscale
# img = cv2.imread("filled.png",0)

# # create window and add trackbar
# cv2.namedWindow('Result')
# cv2.createTrackbar('KernelSize','Result',0,15,doClose)
# # save result
# cv2.imwrite('result.png', img)