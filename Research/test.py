import matplotlib.pyplot as plt
import os
import numpy as np
from scipy.ndimage import rotate
import pyvista as pv
import matplotlib.pyplot as plt
import scipy
from math import radians
from math import cos
from math import sin


sponge = [
        [
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1]
        ],
        [
            [1, 0, 1],
            [0, 0, 0],
            [1, 0, 1]
        ],
        [
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1]
        ]
    ]


wall = [
        [
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 1]
        ],
        [
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 1]
        ],
        [
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 1]
        ]
    ]

def draw(volume):
    # Create the x, y, and z coordinate arrays.  We use
    # numpy's broadcasting to do all the hard work for us.
    # We could shorten this even more by using np.meshgrid.
    x = np.arange(volume.shape[0])[:, None, None]
    y = np.arange(volume.shape[1])[None, :, None]
    z = np.arange(volume.shape[2])[None, None, :]
    x, y, z = np.broadcast_arrays(x, y, z)

    # Turn the volumetric data into an RGB array that's
    # just grayscale.  There might be better ways to make
    # ax.scatter happy.
    c = np.tile(volume.ravel()[:, None], [1, 3])

    # Do the plotting in a single call.
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.scatter(x.ravel(),
               y.ravel(),
               z.ravel(),
               c=c)
    plt.show()

# Rotate the coordinates indices
angle = 30
wall=wall*15
data = np.array(wall, dtype=np.int64)
draw(data)
data_r = scipy.ndimage.interpolation.rotate(data, angle, (1, 2))
draw(data_r)
data_r = scipy.ndimage.interpolation.rotate(data_r, angle, (0, 1))
draw(data_r)