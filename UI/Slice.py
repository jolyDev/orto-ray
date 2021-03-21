import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pyvi
import numpy as np
from Slider import Slider
from PIL import Image

import Render2d

from common.ProjectionTypes import View

import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def array_to_qimage(im: np.ndarray, copy=False):
    gray_color_table = [qRgb(i, i, i) for i in range(256)]

    qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_Indexed8)
    qim.setColorTable(gray_color_table)
    return qim.copy() if copy else qim

def array_to_pixmap(im):
    return QPixmap(array_to_qimage(im))


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class SliceView(QWidget):

    def __init__(self, parent, view: View, data_manager, apply_callback, reset_callback):
        super().__init__()

        self.parent = parent
        self.view = view
        self.data_manager = data_manager
        self.slider = Slider(self, 0, self._GetSliderMax(), self.updateImage)
        self.pixel_area = self.getPixelArea(self.data_manager.getDimetionsSize())

        self.UiComponents()

        self.apply = apply_callback
        self.reset = reset_callback

        # showing all the widgets
        self.show()

        # method for widgets

    def resetAnchorPoint(self, x, y):
        self.reset()

    def setNewAnchorPoint(self, x, y):
        self.apply(self, x, y)

    def rotate(self, image):
        return np.rot90(image, 3)

    def updateImage(self):
        self.image.draw(self.getImage())

    def updateLabelImage(self, anchor, min, max):
        if not anchor:
            self.updateImage()
        else :
            origin = self.getImage()
            labeled = self.data_manager.labeSlice(origin, anchor[0], anchor[1], min, max, self.pixel_area)
            self.image.draw(labeled)

    def UiComponents(self):
        vbox = QVBoxLayout(self)

        self.title = self._GetTitle()
        vbox.addWidget(QLabel(self.title))

        self.image = Render2d.WindowX(self.getImage(), self.setNewAnchorPoint, self.resetAnchorPoint)
        vbox.addWidget(self.image)

        vbox.addWidget(self.slider)

        self.setLayout(vbox)

    def getView(self):
        return self.view

    def getImage(self):
        index = self.slider.getIndex()
        if self.view == View.FRONTAL or self.view == View.HORIZONTAL:
            return self.rotate(self.data_manager.getSlice(index, self.view))
        if self.view == View.PROFILE:
            return self.data_manager.getSlice(index, self.view)

    def getPixelArea(self, width):
        if self.view == View.FRONTAL:
            return width[1] * width[2]
        if self.view == View.HORIZONTAL:
            return width[0] * width[2]
        if self.view == View.PROFILE:
            return width[0] * width[1]

    def _GetTitle(self) -> str:
        if self.view == View.FRONTAL:
            return "Frontal"
        if self.view == View.PROFILE:
            return "Profile"
        if self.view == View.HORIZONTAL:
            return "Horizontal"

    def _GetSliderMax(self):
        return self.data_manager.getMax(self.view)

