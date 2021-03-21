from stl import mesh
import numpy as np
from skimage import measure

# 3D plotting
def make_mesh(image, threshold=1, step_size=1):

    print("Transposing surface")
    p = image.transpose(2, 1, 0)

    print("Calculating surface")
    print(measure.marching_cubes(p, threshold))
    verts, faces, norm, val = measure.marching_cubes(p, threshold, step_size=step_size, allow_degenerate=True)
    #verts, faces = measure.marching_cubes(p, threshold)
    return verts, faces


def save_mesh(filename, vert, ind):
    if (len(vert) % 3) != 0:
        print("incorrect mesh data")
        return

    triangles_count = len(ind) // 3
    data = np.zeros(triangles_count, dtype=mesh.Mesh.dtype)

    for index in range(triangles_count):
        i = ind[3 * index + 0]
        j = ind[3 * index + 1]
        k = ind[3 * index + 2]

        data["vectors"][index] = np.array(
            [[vert[i].x, vert[i].y, vert.vertices[i].z],
             [vert[j].x, vert[j].y, vert.vertices[j].z],
             [vert[k].x, vert[k].y, vert.vertices[k].z]])

    m = mesh.Mesh(data)
    m.save(filename)
    return

def _save_mesh(vertices, faces, filename):
    # Create the mesh
    cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            cube.vectors[i][j] = vertices[f[j], :]

    # Write the mesh to file "cube.stl"
    cube.save(filename)