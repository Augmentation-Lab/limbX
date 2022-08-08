import numpy as np
from scipy import ndimage as ndi
import matplotlib.pyplot as plt

from skimage import data
from skimage.exposure import histogram
coins = data.coins()
hist, hist_centers = histogram(coins)

from skimage.filters import sobel
elevation_map = sobel(coins)
markers = np.zeros_like(coins)
markers[coins < 30] = 1
markers[coins > 150] = 2

from skimage.segmentation import watershed
segmentation = watershed(elevation_map, markers)

segmentation = ndi.binary_fill_holes(segmentation - 1)
# labeled_coins, _ = ndi.label(segmentation)

# loop through the objects to find the center of mass

# labels, _ = ndi.label(segmentation, structure=np.ones((3, 3)))
# label_idx = labels[0, 0]
# mask = (labels == label_idx)
# center = np.array(ndi.center_of_mass(mask, labels, np.arange(label_idx + 1)))
# # plot the center on the image
# fig, ax = plt.subplots(figsize=(4, 3))
# ax.imshow(segmentation, cmap=plt.cm.gray, interpolation='nearest')
# ax.plot(center[:, 1], center[:, 0], 'o')
# ax.axis('off')
# ax.set_title('Center of mass')
# plt.savefig('center_of_mass.png')


# save the labeled coins
# plt.imsave('labeled_coins_1.png', labeled_coins[1])
# plt.imsave('labeled_coins.png', labeled_coins)
# plt.imsave('segmentation.png', segmentation)