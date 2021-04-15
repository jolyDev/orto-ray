from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
from Slider import Slider

import time
import Render2d
from segmentation.segmentation_manager import *
import Algorithms.regionGrowth2D

from Core.Projection import *

def array_to_qimage(im: np.ndarray, copy=False):
    gray_color_table = [qRgb(i, i, i) for i in range(256)]

    qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_Indexed8)
    qim.setColorTable(gray_color_table)
    return qim.copy() if copy else qim

def array_to_pixmap(im):
    return QPixmap(array_to_qimage(im))

class SliceView(QWidget):

    def __init__(self, parent, view: View, dicom, apply_callback, reset_callback, segmentation2d_callback):
        super().__init__()

        plt.set_cmap("gray")
        self.parent = parent
        self.view = view
        self.dicom = dicom
        self.slider = Slider(self, 0, self.dicom.getMax(self.view), segmentation2d_callback)
        self.anchor_apply = apply_callback
        self.image = Render2d.Render2D(self.getImage(), self.apply, reset_callback)
        #self.pixel_area = self.getPixelArea(self.data_manager.getDimetionsSize())

        self.UiComponents()
        self.show()

    def apply(self, x, y):
        self.anchor_apply(self, x, y)

    def rotate(self, image):
        return np.rot90(image, 3)

    def getMinBoundForView(self):
        if (self.view == View.PROFILE):
            min = self.dicom.x_min
            max = self.dicom.x_max
        elif (self.view == View.FRONTAL):
            min = self.dicom.y_min
            max = self.dicom.y_max
        elif (self.view == View.HORIZONTAL):
            min = self.dicom.z_min
            max = self.dicom.z_max

        return (min, max)

    def on3DDataChanged(self):
        min, max = self.getMinBoundForView()
        self.slider.setRange(min, max)
        self.image.draw(self.getImage())

    def resetImage(self):
        self.image.draw(self.getImage())

    def overlay(self, mask):
        self.image.drawOverlayed(self.getImage(), mask)

    def UiComponents(self):
        vbox = QVBoxLayout(self)

        vbox.addWidget(QLabel(view_to_str(self.view)))

        vbox.addWidget(self.image)

        vbox.addWidget(self.slider)

        self.setLayout(vbox)

    def getView(self):
        return self.view

    def getImage(self):
        min, max = self.getMinBoundForView()
        return self.dicom.getSlice(self.slider.getIndex() - int(min), self.view)

    def getPixelArea(self, width):
        if self.view == View.FRONTAL:
            return width[1] * width[2]
        if self.view == View.HORIZONTAL:
            return width[0] * width[2]
        if self.view == View.PROFILE:
            return width[0] * width[1]

