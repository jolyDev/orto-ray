import matplotlib.pyplot as plt
import os
import numpy as np
from scipy.ndimage import rotate
import pyvista as pv
import matplotlib.pyplot as plt


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
            [1, 1, 1],
            [0, 0, 0],
            [1, 1, 1]
        ],
        [
            [1, 1, 1],
            [0, 0, 0],
            [1, 1, 1]
        ],
        [
            [1, 1, 1],
            [0, 0, 0],
            [1, 1, 1]
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


def rotate_nn(data, angle, axes):
    """
    Rotate a `data` based on rotating coordinates.
    """

    # Create grid of indices
    shape = data.shape
    d1, d2, d3 = np.mgrid[0:shape[0], 0:shape[1], 0:shape[2]]

    # Rotate the indices
    d1r = rotate(d1, angle=angle, axes=axes, mode='constant', cval=4)
    d2r = rotate(d2, angle=angle, axes=axes, mode='constant', cval=4)
    d3r = rotate(d3, angle=angle, axes=axes, mode='constant', cval=4)

    # Round to integer indices
    d1r = np.round(d1r)
    d2r = np.round(d2r)
    d3r = np.round(d3r)

    d1r = np.clip(d1r, 0, 10)
    d2r = np.clip(d2r, 0, 10)
    d3r = np.clip(d3r, 0, 10)

    return data[d1r, d2r, d3r]

# Rotate the coordinates indices
angle = 45
wall=wall*10
data = np.array(wall, dtype=np.int64)
axes = (0, 1)
draw(data)
data_r = rotate_nn(data, angle, axes)
draw(data_r)