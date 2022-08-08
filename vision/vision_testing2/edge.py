import numpy as np
import matplotlib.pyplot as plt
from skimage import data
import cv2
# coins = data.coins()
coins = cv2.imread("mouse.png")
coins = cv2.cvtColor(coins, cv2.COLOR_BGR2GRAY)
hist = np.histogram(coins, bins=np.arange(0, 256))
fig, (ax1) = plt.subplots()
ax1.imshow(coins, cmap=plt.cm.gray,interpolation='nearest')

from skimage.filters import sobel
elevation_map = sobel(coins)
fig, ax = plt.subplots(figsize=(4, 3))
ax.imshow(elevation_map, cmap=plt.cm.gray, interpolation='nearest')
ax.axis('off')
ax.set_title('elevation_map')
plt.imsave('elevation_map.png', elevation_map)

from skimage.feature import canny
newcoins = cv2.imread("elevation_map.png")
newcoins = cv2.cvtColor(newcoins, cv2.COLOR_BGR2GRAY)
edges = canny(newcoins/255.)
fig, ax = plt.subplots(figsize=(4, 3))
ax.imshow(edges, cmap=plt.cm.gray, interpolation='nearest')
ax.axis('off')
ax.set_title('Canny detector')

from scipy import ndimage as ndi
fill_coins = ndi.binary_fill_holes(edges)
fig, ax = plt.subplots(figsize=(4, 3))
ax.imshow(fill_coins, cmap=plt.cm.gray, interpolation='nearest')
ax.axis('off')
ax.set_title('Filling the holes')

plt.imsave('fill_coins.png', fill_coins)
plt.imsave('edges.png', edges)