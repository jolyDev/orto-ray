import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pyvi

import numpy as np

from Slice import SliceView, View
from hu_manager import HounsfieldUnitsManager
from segmentation.segmentation_manager import SegmentationManager
from segmentation.segmantate3D import segmentate3D
from segmentation.segmantate3D import test
from MultiSelection.AnchorPoints import AnchorPointsManager

from segmentation.china import regionGrowing

from Segmentation3D.RegionGrowth import RegionGrow3D

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LightSource
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import scipy.ndimage
from skimage import morphology
from skimage import measure
from skimage.morphology import square

# 3D plotting
def make_mesh(image, threshold=-300, step_size=1):
    print("Transposing surface")
    p = image.transpose(2, 1, 0)

    print("Calculating surface")
    print(measure.marching_cubes(p, threshold))
    verts, faces, norm, val = measure.marching_cubes(p, threshold, step_size=step_size, allow_degenerate=True)
    # verts, faces = measure.marching_cubes(p, threshold)
    return verts, faces

def normalize(arr):
    arr_min = np.min(arr)
    return (arr-arr_min)/(np.max(arr)-arr_min)

class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.anchor_manager = AnchorPointsManager()

        self.dicom_manager = SegmentationManager("E:/orto-ray/dicom_data/head")
        self.frontal_view = SliceView(self, View.FRONTAL, self.dicom_manager, self.anchor_manager.apply, self.anchor_manager.reset)
        self.profile_view = SliceView(self, View.PROFILE, self.dicom_manager, self.anchor_manager.apply, self.anchor_manager.reset)
        self.horizontal_view = SliceView(self, View.HORIZONTAL, self.dicom_manager, self.anchor_manager.apply, self.anchor_manager.reset)

        self.anchor_manager.addListener(self.frontal_view)
        self.anchor_manager.addListener(self.profile_view)
        self.anchor_manager.addListener(self.horizontal_view)

        self.hu_manager = HounsfieldUnitsManager(self.anchor_manager.onHU_BoundsChanged)

        #self.model = SliceView(self, "model", r'C:\athena.jpg')
        self.setWindowTitle("Ortho Ray")
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

    def regenerate3d(self):

        x = self.frontal_view.slider.getIndex()
        y = self.profile_view.slider.getIndex()
        z = self.horizontal_view.slider.getIndex()

        data3d = self.dicom_manager.getData()
        seeds = self.anchor_manager.anchors
        seeds = [[x, y, z]]
        max = self.hu_manager.slider.getMax()
        min = self.hu_manager.slider.getMin()
        sengmented_area = segmentate3D(data3d, seeds, max, min)

    def UiComponents(self):
        hbox = QHBoxLayout(self)

        grid = QGridLayout(self)

        grid.addWidget(self.horizontal_view,0,0)
        grid.addWidget(QWidget(),0,1)
        grid.addWidget(self.profile_view,1,0)
        grid.addWidget(self.frontal_view,1,1)

        button = QPushButton('regenerate 3d')
        button.clicked.connect(self.regenerate3d)
        grid.addWidget(button,0,2)

        hbox.addLayout(grid)
        hbox.addWidget(self.hu_manager)
        self.showMaximized()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
