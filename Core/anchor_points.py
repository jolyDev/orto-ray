import Core.Projection as core
import numpy as np

def getRaw2D(points, view):
    points2d = []
    for el in points:
        points2d.append(el.get2d(view))

    raw = []
    for el in points2d:
        raw.append([el.x, el.y])

    return np.array(raw, dtype=np.int64)

class AnchorPointsManager:

    def __init__(self, callback):
        self.anchors = []
        self.callback = callback

    def reset(self):
        self.anchors = []
        self.callback()

    def apply(self, slice, coord_1, coord_2):
        point2d = core.point2d(coord_1, coord_2, slice.view)
        point3d = point2d.to3d(slice.slider.getIndex())
        self.reset()
        self.anchors.append(point3d)
        self.callback()

    def getRaw3D(self):
        raw = []
        for el in self.anchors:
            raw.append([el.x, el.y, el.z])

        return np.array(raw, dtype=np.int64)

    def getRaw2D(self, view):
        return getRaw2D(self.anchors, view)


