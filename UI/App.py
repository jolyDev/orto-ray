import sys
from PyQt5.QtWidgets import *
import time
import numpy as np
import pyvista as pv

from SliceView import SliceView, View
from hu_manager import HounsfieldUnitsManager
from segmentation.segmentation_manager import SegmentationManager
from segmentation.segmantate3D import test
from Core.anchor_points import AnchorPointsManager
from Core.DicomDataManager import DicomDataManager

import Segmentation3D.regionGrowth2D
import Segmentation3D.regionGrowth3D
import matplotlib.pyplot as plt
from matplotlib import cm
from DataView import DataView
import Render3d

from skimage import measure

import Core.render3d as render3d

def axis_log(point, data3d):
    x = point[0][0]
    y = point[0][1]
    z = point[0][2]
    print("[" + str(x) + ", " + str(y) + ", " + str(z) + "] | " + str(data3d[x][y][z]))

def normalize(arr):
    arr_min = np.min(arr)
    return (arr-arr_min)/(np.max(arr)-arr_min)

class Window(QWidget):

    def __init__(self):
        super().__init__()
        plt.set_cmap("gray")

        self.anchors = AnchorPointsManager()
        self.hu_manager = HounsfieldUnitsManager(self.anchors.on_hu_bounds_changed)
        self.dicom = DicomDataManager("E:/orto-ray/dicom_data/head")
        self.render_widget = DataView(self.dicom, self.anchors, self.hu_manager)

        self.frontal_view = SliceView(self, View.FRONTAL, self.dicom, self.anchors.apply, self.anchors.reset)
        self.profile_view = SliceView(self, View.PROFILE, self.dicom, self.anchors.apply, self.anchors.reset)
        self.horizontal_view = SliceView(self, View.HORIZONTAL, self.dicom, self.anchors.apply, self.anchors.reset)

        self.anchors.addListener(self.frontal_view)
        self.anchors.addListener(self.profile_view)
        self.anchors.addListener(self.horizontal_view)

        self.UiComponents()
        self.show()

    def updateLabeling(self, min, max):
        self.frontal_view.updateLabelImage(min, max)
        self.profile_view.updateLabelImage(min, max)
        self.horizontal_view.updateLabelImage(min, max)

    def show_histogram(self, values):
        n, bins, patches = plt.hist(values.reshape(-1), 50, density=True)
        bin_centers = 0.5 * (bins[:-1] + bins[1:])

        for c, p in zip(normalize(bin_centers), patches):
            plt.setp(p, 'facecolor', cm.viridis(c))

        plt.show()

    def UiComponents(self):
        self.setWindowTitle("Ortho Ray")

        hbox = QHBoxLayout(self)

        grid = QGridLayout(self)

        grid.addWidget(self.horizontal_view,0,0)
        grid.addWidget(self.profile_view,1,0)
        grid.addWidget(self.frontal_view,1,1)

        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 1)

        hbox.addWidget(self.render_widget)
        hbox.addLayout(grid)
        hbox.addWidget(self.hu_manager)
        self.showMaximized()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
