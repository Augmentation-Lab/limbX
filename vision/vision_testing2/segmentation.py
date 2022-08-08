import numpy as np
from scipy import ndimage as ndi
import matplotlib.pyplot as plt
import cv2

from skimage import data
from skimage.exposure import histogram
# coins = data.coins()
coins = cv2.imread("mouse.png")
coins = cv2.cvtColor(coins, cv2.COLOR_BGR2GRAY)
hist, hist_centers = histogram(coins)

from skimage.filters import sobel
elevation_map = sobel(coins)
markers = np.zeros_like(coins)
# TODO: automate this thresholding
markers[coins < 30] = 1
markers[coins > 150] = 2

from skimage.segmentation import watershed
segmentation = watershed(elevation_map, markers)

segmentation_all = ndi.binary_fill_holes(segmentation - 1)
# TODO: filter out small objects
from skimage import morphology
segmentation = morphology.remove_small_objects(segmentation_all, 21)
plt.imsave('segmentation.png', segmentation)

# im_in = cv2.imread("segmentation.png", cv2.IMREAD_GRAYSCALE);
# th, im_th = cv2.threshold(im_in, 150, 255, cv2.THRESH_BINARY_INV);
# im_floodfill = im_th.copy()
# h, w = im_th.shape[:2]
# mask = np.zeros((h+2, w+2), np.uint8)
# cv2.floodFill(im_floodfill, mask, (0,0), 255);
# plt.imsave('filled.png', im_floodfill)

labeled_coins, _ = ndi.label(segmentation)

# loop through the segmented objects
fig, ax = plt.subplots(figsize=(4, 3))
for label_idx in range(1, labeled_coins.max() + 1):
    # find the center of mass of each object
    mask = (labeled_coins == label_idx)
    center = np.array(ndi.center_of_mass(mask, labeled_coins, np.arange(label_idx + 1)))
    # plot the center on the image
    ax.plot(center[:, 1], center[:, 0], 'o')
ax.imshow(segmentation, cmap=plt.cm.gray, interpolation='nearest')
ax.axis('off')
ax.set_title('Center of mass')
plt.savefig('center_of_mass.png')


# save the labeled coins
plt.imsave('labeled_coins.png', labeled_coins)
# plt.imsave('segmentation.png', segmentation)