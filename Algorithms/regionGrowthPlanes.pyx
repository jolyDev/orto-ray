from collections import deque
import numpy as np
cimport numpy as np
cimport cython

def axis_log(point, data3d):
    x = point[0][0]
    y = point[0][1]
    z = point[0][2]
    print("[" + str(x) + ", " + str(y) + ", " + str(z) + "] | " + str(data3d[x][y][z]))

cdef _IsBelongToPlane(int jx, int jy, int jz ,int x, int y, int z):
    return jx == x or jy == y or jz == z

cdef _isInBounds(bounds, int x, int y, int z):
    return x < bounds[0] and y < bounds[1] and z < bounds[2] and x > -1 and y > -1 and z > -1

cdef _isInRange(int value, int max, int min):
    return value < max and value > min

cdef _expand(np.int64_t[:,:,:] data, np.int64_t[:,:,:] output, queue, int jx, int jy, int jz ,int x, int y, int z, int max, int min):
    if _isInBounds(data.shape, x, y, z):
        if _IsBelongToPlane(jx, jy, jz, x, y, z):
            if _isInRange(data[x][y][z], max, min) and output[x][y][z] == 0:
                output[x][y][z] = 1
                queue.append([x, y, z])

def segmentatePlanes(np.int64_t[:,:,:] data3d, planes_joint, np.int64_t[:,:] seeds, int max, int min):
    axis_log(seeds, data3d)
    mask = np.zeros_like(data3d)
    queue = deque()

    cdef int jx = planes_joint[0]
    cdef int jy = planes_joint[1]
    cdef int jz = planes_joint[2]

    for seed in seeds:
        if _isInBounds(data3d.shape, seed[0], seed[1], seed[2]):
            if _isInRange(data3d[seed[0]][seed[1]][seed[2]], max, min):
                mask[seed[0], seed[1], seed[2]] = 1
                queue.append([seed[0], seed[1], seed[2]])

    cdef int front[3]
    cdef int near[6][3]
    cdef int x
    cdef int y
    cdef int z

    while len(queue) != 0:
        front = queue.pop()
        x = front[0]
        y = front[1]
        z = front[2]

        near[0][0] = x-1
        near[0][1] = y
        near[0][2] = z

        near[1][0] = x+1
        near[1][1] = y
        near[1][2] = z

        near[2][0] = x
        near[2][1] = y-1
        near[2][2] = z

        near[3][0] = x
        near[3][1] = y+1
        near[3][2] = z

        near[5][0] = x
        near[5][1] = y
        near[5][2] = z-1

        near[6][0] = x
        near[6][1] = y
        near[6][2] = z+1

        for item in near:
            _expand(data3d, mask, queue, jx, jy, jz, item[0], item[1], item[2], max, min)

    return mask
