from collections import deque
import numpy as np
cimport numpy as np
cimport cython

def axis_log(point, data3d):
    x = point[0][0]
    y = point[0][1]
    z = point[0][2]
    print("[" + str(x) + ", " + str(y) + ", " + str(z) + "] | " + str(data3d[x][y][z]))

cdef _isInBounds(int value, int max, int min):
    return value < max and value > min

cdef _expand(np.int64_t[:,:,:] data, np.int64_t[:,:,:] output, queue, int x, int y, int z, int max, int min):
    bounds = data.shape
    if x < bounds[0] and y < bounds[1] and z < bounds[2]:
        if x > -1 and y > -1 and z > -1:
            if _isInBounds(data[x][y][z], max, min) and output[x][y][z] == 0:
                output[x][y][z] = 1
                queue.append([x, y, z])

cdef int[:,:] _getNear(x, y, z):
    return np.array([
        [x-1, y,   z],
        [x+1, y,   z],
        [x,   y-1, z],
        [x,   y+1, z],
        [x,   y,   z-1],
        [x,   y,   z+1]
    ])


def segmentate3D(np.int64_t[:,:,:] data3d, np.int64_t[:,:] seeds, int max, int min):
    axis_log(seeds, data3d)
    mask = np.zeros_like(data3d)
    queue = deque()

    for seed in seeds:
        if _isInBounds(data3d[seed[0]][seed[1]][seed[2]], max, min):
            mask[seed[0], seed[1], seed[2]] = 1
            queue.append([seed[0], seed[1], seed[2]])

    while len(queue) != 0:
        front = queue.pop()
        near = _getNear(front[0], front[1], front[2])
        for item in near:
            _expand(data3d, mask, queue, item[0], item[1], item[2], max, min)

    return mask

cdef _expand2d(np.int64_t[:,:] data, np.int64_t[:,:] output, queue, int x, int y, int max, int min):
    bounds = data.shape
    if x < bounds[0] and y < bounds[1]:
        if x > -1 and y > -1:
            if _isInBounds(data[x][y], max, min) and output[x][y] == 0:
                output[x][y] = 1
                queue.append([x, y])

cdef int[:,:] _getNear2d(x, y):
    return np.array([
        [x-1, y, ],
        [x+1, y, ],
        [x,   y-1],
        [x,   y+1]
    ])

def segmentate2d(np.int64_t[:,:] data2d, np.int64_t[:,:] seeds, int max, int min):
    mask = np.zeros_like(data2d)
    queue = deque()

    for seed in seeds:
        if _isInBounds(data2d[seed[0]][seed[1]], max, min):
            mask[seed[0], seed[1]] = 1
            queue.append([seed[0], seed[1]])

    while len(queue) != 0:
        front = queue.pop()
        near = _getNear2d(front[0], front[1])
        for item in near:
            _expand2d(data2d, mask, queue, item[0], item[1], max, min)

    return mask
