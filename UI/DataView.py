from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from SliderX import SliderX
from Core.Projection import View
from Segmentation3D.regionGrowth3D import segmentate3D
import time
import numpy as np
from Render3d import Render3D

class DataView(QWidget):

    def __init__(self, data3d, anchors, hu):
        super().__init__()

        self.data3d = data3d
        self.anchors = anchors
        self.hu = hu
        self.scene = Render3D(self.data3d.get())
        self.segmented = None

        x_bound = self.data3d.getMax(View.FRONTAL)
        y_bound = self.data3d.getMax(View.PROFILE)
        z_bound = self.data3d.getMax(View.HORIZONTAL)

        self.profile_range    = SliderX(0, x_bound, self.visibilityBoundsChanged)
        self.vertical_range   = SliderX(0, y_bound, self.visibilityBoundsChanged)
        self.horizontal_range = SliderX(0, z_bound, self.visibilityBoundsChanged)

        self.UiComponents()

        self.show()

    def visibilityBoundsChanged(self, min, max):
        #self.renderer.update(self._trimBounds(self.segmented))
        print(min, max)

    def _trimBounds(self, data3d):
        x = self.profile_range
        y = self.vertical_range
        z = self.horizontal_range

        trimmed_data = np.zeros((x.getMax() - x.getMin(), y.getMax() - y.getMin(), z.getMax() - z.getMin()))
        trimmed_data = np.array(trimmed_data, dtype=np.int64)

        for i in range(x.getMin(), x.getMax()):
            for j in range(y.getMin(), y.getMax()):
                for k in range(z.getMin(), z.getMax()):
                    shifted_i = i - x.getMin()
                    shifted_j = j - y.getMin()
                    shifted_k = k - z.getMin()
                    trimmed_data[0]
                    trimmed_data[0][1]
                    trimmed_data[0][1][2]
                    trimmed_data[shifted_i, shifted_j, shifted_k] = data3d[i, j, k]

        return np.array(trimmed_data, dtype=np.int64)

    def update(self):
        self.scene.update(self._trimBounds(self.data3d.get()))

    def regenerate3d(self):
        start = time.time()
        data3d = self._trimBounds(self.data3d.get())

        mask = segmentate3D(data3d, self.anchors.get(), self.hu.slider.getMax(), self.hu.slider.getMin())
        filter_condition = mask == 0
        segmented = np.copy(data3d)
        segmented[filter_condition] = 0

        end = time.time()
        print(end - start)
        self.scene.update(segmented)

    def UiComponents(self):
        vbox = QVBoxLayout(self)

        vbox.addWidget(QLabel("3D view"))

        vbox.addWidget(self.scene)
        vbox.addWidget(self.profile_range)
        vbox.addWidget(self.vertical_range)
        vbox.addWidget(self.horizontal_range)

        button = QPushButton('Regenerate 3D')
        button.clicked.connect(self.regenerate3d)

        button2 = QPushButton('Bounds 3D')
        button2.clicked.connect(self.update)

        vbox.addWidget(button)
        vbox.addWidget(button2)

        self.setLayout(vbox)