
import matplotlib.pyplot as plt
import numpy as np

import Mesh.saveToSTL as mesh_manager

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

def use():

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

    indexes = [[1,1,1]]

    num_arr = np.array(arr, dtype=np.int64)
    index_array = np.array(indexes, dtype=np.int64)

    var = RegionGrowth.RegionGrow3D(num_arr, 6, 4, "6n")

    return np.asarray(var.main(index_array))


def test_stl_saving():
    segmented = use()
    mesh_manager.to_mesh(segmented, r"E:/orto-ray/Segmentation3D/km2.stl")
    #mesh_manager.save_stl(mesh_manager)

if __name__ == '__main__':
    #segmented = use()
    #test(segmented)
    test_stl_saving()