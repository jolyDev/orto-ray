from collections import deque
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy.ndimage
from skimage import morphology
from skimage import measure
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.colors import LightSource

def _isInBounds(value, max, min):
    return value < max and value > min

def _expand(data, output, queue, x: int, y: int, z: int, max, min):
    bounds = data.shape
    if x < bounds[0] and y < bounds[1] and z < bounds[2]:
        if x > -1 and y > -1 and z > -1:
            if _isInBounds(data[x][y][z], max, min) and output[x][y][z] == 0:
                output[x][y][z] = 1
                queue.append([x, y, z])

def _getNear(data, x, y, z):
    return [
        [x-1, y,   z],
        [x+1, y,   z],
        [x,   y-1, z],
        [x,   y+1, z],
        [x,   y,   z-1],
        [x,   y,   z+1],
    ]

def segmentate3D(data3d, seeds, max, min):
    mask = np.zeros_like(data3d)
    queue = deque()

    for seed in seeds:
        if _isInBounds(data3d[seed[0]][seed[1]][seed[2]], max, min):
            mask[seed[0], seed[1], seed[2]] = 1
            queue.append((seed[0], seed[1], seed[2]))

    while len(queue) != 0:
        front = queue.pop()
        near = _getNear(data3d, front[0], front[1], front[2])
        print(front[0], front[1], front[2])
        for item in near:
            _expand(data3d, mask, queue, item[0], item[1], item[2], max, min)

    return mask

def test(data):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    linear = data.reshape(-1)
    # your real data here - some 3d boolean array
    #x = linear[::3]
    #y = linear[1::3]
    #y = linear[1::3]
    #z = np.indices((10, 10, 10))
    #voxels = (x == y) | (y == z)

    ax.voxels(data)

    plt.show()


arr =  [[
    [5,  5, 0],
    [0,  5, 0],
    [0,  0, 0]],

   [[0, 5, 0],
    [5, 5, 5],
    [0, 5, 0]],

   [[0, 0, 0],
    [0, 5, 0],
    [0, 0, 0]]]

num_arr = np.array(arr)
test(num_arr)

segmented = segmentate3D(num_arr, [[1,1,1]], 6, 4)

test(segmented)
