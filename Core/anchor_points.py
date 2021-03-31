import Core.Projection as core
import numpy as np

class AnchorPointsManager:

    def __init__(self):
        self.anchors = []
        self.listeners = []
        self.min = 0
        self.max = 1

    def on_hu_bounds_changed(self, min: int, max: int):
        self.min = min
        self.max = max
        self.update()

    def reset(self):
        self.anchors = []

    def apply(self, slice, coord_1, coord_2):
        data2d = slice.getImage()
        print("2D view")
        print("{} | {} :".format(coord_1, coord_2))
        print(data2d.shape)
        print(data2d[int(coord_1)][int(coord_2)])

        point2d = core.point2d(coord_1, coord_2, slice.view)
        point3d = point2d.to3d(slice.slider.getIndex())
        self.reset()
        self.anchors.append(point3d)

    def get(self):
        raw = []
        for el in self.anchors:
            raw.append([el.x, el.y, el.z])

        return np.array(raw, dtype=np.int64)

    def addListener(self, listener):
        listener.slider.value.valueChanged.connect(self.update)
        self.listeners.append(listener)

    def update(self):
        for subscriber in self.listeners:
            subscriber.updateSegmentation(self.anchors, self.min, self.max)

