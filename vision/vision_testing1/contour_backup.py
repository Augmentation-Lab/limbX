import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageEnhance

#read the image
im = Image.open("mouse.png")
#image brightness enhancer
enhancer = ImageEnhance.Contrast(im)
factor = 5 #increase contrast
im_output = enhancer.enhance(factor)
im_output.save("contrast_adapter.png")

# read the image
# image = cv2.imread('input/image_1.jpg')
image = cv2.imread('contrast_adapter.png')
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# detect the contours on the binary image using cv2.CHAIN_APPROX_NONE

# SEGMENT IMAGE BY COLOR OUTLINES
# # convert the image to grayscale format
# img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# # apply binary thresholding
# ret, thresh = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY)
# # visualize the binary image
# cv2.imwrite('image_thres1.jpg', thresh)
# thresh = np.invert(thresh)

from skimage.filters import sobel
elevation_map = sobel(image)
fig, ax = plt.subplots(figsize=(4, 3))
ax.imshow(elevation_map, cmap=plt.cm.gray, interpolation='nearest')
ax.axis('off')
ax.set_title('elevation_map')
plt.imsave('elevation_map.png', elevation_map)

# # erosion
# kernel = np.ones((10,10), np.uint8)
# img_erosion = cv2.erode(thresh, kernel, iterations=1)
# kernel_fill = np.ones((20,20), np.uint8)
# img_dilation = cv2.dilate(img_erosion, kernel_fill, iterations=1)
# # save images
# cv2.imwrite('image_erosion.jpg', img_erosion)
# cv2.imwrite('image_dilation.jpg', img_dilation)

# from scipy import ndimage as ndi
# filled = ndi.binary_fill_holes(img_dilation)
# # save images
# plt.imsave('image_filled.jpg', filled)

# contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
                                     
# # draw contours on the original image
# image_copy = image.copy()
# cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
               
# # see the results
# # cv2.imshow('None approximation', image_copy)
# # cv2.waitKey(0)
# cv2.imwrite('contours_none_image1.jpg', image_copy)