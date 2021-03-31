from collections import deque
import numpy as np
cimport numpy as np
cimport cython

cdef _isInBounds(int value, int max, int min):
    return value < max and value > min

cdef _expand2d(np.int64_t[:,:] data, np.int64_t[:,:] output, queue, int x, int y, int max, int min):
    bounds = data.shape
    if x < bounds[0] and y < bounds[1]:
        if x > -1 and y > -1:
            if _isInBounds(data[x][y], max, min) and output[x][y] == 0:
                output[x][y] = 1
                queue.append([x, y])

def segmentate2d(np.int64_t[:,:] data2d, np.int64_t[:,:] seeds, int max, int min):
    cdef np.int64_t[:,:] mask = np.zeros_like(data2d)
    queue = deque()

    for seed in seeds:
        if _isInBounds(data2d[seed[0]][seed[1]], max, min):
            mask[seed[0], seed[1]] = 1
            queue.append([seed[0], seed[1]])

    cdef int front[2]
    cdef int near[4][2]
    cdef int x
    cdef int y

    while len(queue) != 0:
        front = queue.pop()
        x = front[0]
        y = front[1]
        near[0][0] = x-1
        near[0][1] = y
        near[1][0] = x+1
        near[1][1] = y
        near[2][0] = x
        near[2][1] = y-1
        near[3][0] = x
        near[3][1] = y+1

        for item in near:
            _expand2d(data2d, mask, queue, item[0], item[1], max, min)

    return mask
