from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from SliderX import SliderX
from Core.Projection import View
from Algorithms.regionGrowth3D import segmentate3D
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

    def _trimBounds(self):
        x = self.profile_range
        y = self.vertical_range
        z = self.horizontal_range

        #self.scene.update(self.data3d.trim(x.getMax(), x.getMin(), y.getMax(), y.getMin(), z.getMax(), z.getMin()))

        d = self.data3d.trim(x.getMax(), x.getMin(), y.getMax(), y.getMin(), z.getMax(), z.getMin())
        for x in range(d.shape[0]):
            for y in range(d.shape[1]):
                for z in range(d.shape[2]):
                    if x != 300 and y != 300 and z != 30:
                        d[x, y, z] = 0

        self.scene.update(d)

    def update(self):

        d = self._trimBounds()
        for x in range(d.shape[0]):
            for y in range(d.shape[1]):
                for z in range(d.shape[2]):
                    if x != 50 or y != 50 or z != 50:
                        d[x, y, z] = 0

        self.scene.update(d)

    def rotate(self):
        self.scene.update(self.data3d.getRotated((self.angle_x.value(), self.angle_y.value(), self.angle_z.value())))

        self.profile_range.setMinBound(0)
        self.profile_range.setMin(0)
        self.profile_range.setMaxBound(self.data3d.getMaxModified(View.FRONTAL))
        self.vertical_range.setMin(0)
        self.vertical_range.setMinBound(0)
        self.vertical_range.setMaxBound(self.data3d.getMaxModified(View.PROFILE))
        self.horizontal_range.setMin(0)
        self.horizontal_range.setMinBound(0)
        self.horizontal_range.setMaxBound(self.data3d.getMaxModified(View.HORIZONTAL))

    def reset(self):
        self.data3d.resetModification()
        self.scene.update(self.data3d.getModified())

    def regenerate3d(self):

        if len(self.anchors.getRaw3D()) == 0:
            return

        start = time.time()
        data3d = self.data3d.getModified()

        mask = segmentate3D(data3d, self.anchors.getRaw3D(), self.hu.slider.getMax(), self.hu.slider.getMin())
        filter_condition = mask == 0
        segmented = np.copy(data3d)
        segmented[filter_condition] = 0

        end = time.time()
        print(end - start)
        if np.count_nonzero(segmented) == 0:
            self.scene.update(np.array([[[0]]], dtype=np.int64))
        else:
            self.scene.update(segmented)

    def UiComponents(self):
        vbox = QVBoxLayout(self)

        vbox.addWidget(QLabel("3D view"))

        vbox.addWidget(self.scene)
        vbox.addWidget(self.profile_range)
        vbox.addWidget(self.vertical_range)
        vbox.addWidget(self.horizontal_range)


        regenerate = QPushButton('Regenerate 3D')
        regenerate.clicked.connect(self.regenerate3d)

        bounds_update = QPushButton('Bounds 3D')
        bounds_update.clicked.connect(self._trimBounds)

        reset_modifications = QPushButton('Reset modification')
        reset_modifications.clicked.connect(self.reset)

        update_buttons_box = QHBoxLayout(self)
        update_buttons_box.addWidget(regenerate)
        update_buttons_box.addWidget(bounds_update)
        update_buttons_box.addWidget(reset_modifications)

        vbox.addLayout(update_buttons_box)

        rotation_box = QHBoxLayout(self)

        self.angle_x = QSpinBox(self)
        self.angle_y = QSpinBox(self)
        self.angle_z = QSpinBox(self)

        apply_rotation = QPushButton('Apply rotation')
        apply_rotation.clicked.connect(self.rotate)

        rotation_box.addWidget(QLabel("Rotation:"))
        rotation_box.addWidget(QLabel("x = "))
        rotation_box.addWidget(self.angle_x)
        rotation_box.addWidget(QLabel("y = "))
        rotation_box.addWidget(self.angle_y)
        rotation_box.addWidget(QLabel("z = "))
        rotation_box.addWidget(self.angle_z)
        rotation_box.addWidget(apply_rotation)

        vbox.addLayout(rotation_box)

        self.setLayout(vbox)