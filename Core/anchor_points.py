import Core.projection as core

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
        point2d = core.point_2d(slice.view, coord_1, coord_2)
        point3d = point2d.to3d(slice.slider.getIndex())
        self.anchors.append(point3d)

    def addListener(self, listener):
        listener.slider.value.valueChanged.connect(self.update)
        self.listeners.append(listener)

    def update(self):
        for subscriber in self.listeners:
            subscriber.updateSegmentation(self.anchors, self.min, self.max)
