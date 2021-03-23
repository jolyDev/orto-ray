from common.ProjectionTypes import View


class AnchorPointsManager:

    def __init__(self):
        self.anchors = []
        self.listeners = []
        self.min = 0
        self.max = 1

    def onHU_BoundsChanged(self, min: int, max: int):
        self.min = min
        self.max = max
        self.update()

    def reset(self):
        self.anchors = []


    # profile -> y
    # horizontal -> x
    #frontal -> z

    def add_data(self, data):
        self.data = data

    def apply(self, slice, coord_1, coord_2):
        point_3d = []

        index = slice.slider.getIndex()
        if slice.getView() == View.FRONTAL:
            point_3d = [index, coord_1, coord_2]
        if slice.getView() == View.HORIZONTAL:
            point_3d = [coord_1, index, coord_2]
        if slice.getView() == View.PROFILE:
            point_3d = [coord_1, coord_2, index]

        print(point_3d)
        print(self.data[0][1][2])
        print([point_3d[0], point_3d[2], point_3d[1]])
        print(self.data[0][2][1])
        self.anchors = point_3d

    def addListener(self, listener):
        listener.slider.value.valueChanged.connect(self.update)
        self.listeners.append(listener)

    def update(self):
        for subscriber in self.listeners:
            point_2d = self.get2dCoords(subscriber.getView())
            if point_2d:
                subscriber.updateLabelImage(point_2d, self.min, self.max)

    def getCoord3D(self):
        x = self.anchors
        return x

    def get2dCoords(self, view: View):
        if not self.anchors:
            return []

        if view == View.FRONTAL:
            return [self.anchors[1], self.anchors[2]]
        if view == View.HORIZONTAL:
            return [self.anchors[0], self.anchors[2]]
        if view == View.PROFILE:
            return [self.anchors[0], self.anchors[1]]

        return []
