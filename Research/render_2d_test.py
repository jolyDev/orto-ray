import numpy as np
mask = np.zeros((10,10))
mask[3:-3, 3:-3] = 1 # white square in black background
im = np.zeros_like(mask) # random image
masked = np.ma.masked_where(mask == 0, mask)
masked[4][4] = False

import matplotlib.pyplot as plt
plt.figure()
plt.subplot(1,2,1)
plt.imshow(im, 'gray', interpolation='none')
plt.subplot(1,2,2)
plt.imshow(im, 'gray', interpolation='none')
plt.imshow(masked, 'copper', interpolation='none', alpha=0.7)
plt.show()