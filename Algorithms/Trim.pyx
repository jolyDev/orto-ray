from collections import deque
import numpy as np
cimport numpy as np
cimport cython

def Trim(np.int64_t[:,:,:] data3d, int x_max, int x_min, int y_max, int y_min, int z_max, int z_min):
        trimmed = np.zeros((x_max - x_min, y_max - y_min, z_max - z_min))
        trimmed = np.array(trimmed, dtype=np.int64)

        cdef int shifted_i
        cdef int shifted_j
        cdef int shifted_k

        cdef int i
        cdef int j
        cdef int k

        for i in range(x_min, x_max):
            for j in range(y_min, y_max):
                for k in range(z_min, z_max):
                    shifted_i = i - x_min
                    shifted_j = j - y_min
                    shifted_k = k - z_min
                    trimmed[shifted_i, shifted_j, shifted_k] = data3d[i, j, k]

        return trimmed