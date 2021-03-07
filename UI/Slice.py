import sys
from enum import Enum

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pyvi
import numpy as np
from Slider import Slider
from PIL import Image

import Render2d

from segmentation.image_operations import ImageMutator

import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def array_to_qimage(im: np.ndarray, copy=False):
    gray_color_table = [qRgb(i, i, i) for i in range(256)]

    qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_Indexed8)
    qim.setColorTable(gray_color_table)
    return qim.copy() if copy else qim

def array_to_pixmap(im):
    return QPixmap(array_to_qimage(im))

class View(Enum):
    FRONTAL = 0
    PROFILE = 1
    HORIZONTAL = 2

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class SliceView(QWidget):

    def _GetTitle(self) -> str:
        if self.view == View.FRONTAL:
            return "Frontal"
        if self.view == View.PROFILE:
            return "Profile"
        if self.view == View.HORIZONTAL:
            return "Horizontal"

    def _GetSliderMax(self):
        if self.view == View.FRONTAL:
            return self.data_manager.getMaxX()
        if self.view == View.HORIZONTAL:
            return self.data_manager.getMaxY()
        if self.view == View.PROFILE:
            return self.data_manager.getMaxZ()

    def __init__(self, parent, view: View, data_manager, hu_range):
        super(QWidget, self).__init__(parent)

        self.view = view
        self.image_data_operator = ImageMutator()
        self.image_data_operator.getContour()
        self.data_manager = data_manager
        self.slider = Slider(self, 0, self._GetSliderMax(), self.update)
        self.hu = hu_range

        self.UiComponents()

        self.anchor = None

        # showing all the widgets
        self.show()

        # method for widgets

    def resetAnchorPoint(self, x, y):
        self.anchor = None

    def setNewAnchorPoint(self, x, y):
        self.anchor = Point(x, y)

    def rotate(self, image):
        return np.rot90(image, 3)

    def getImage(self):
        index = self.slider.getIndex()
        if self.view == View.FRONTAL:
            return self.rotate(self.data_manager.getSliceYZ(index))
        if self.view == View.HORIZONTAL:
            return self.rotate(self.data_manager.getSliceXZ(index))
        if self.view == View.PROFILE:
            return self.data_manager.getSliceXY(index)

    def update(self):
        if self.anchor is None:
            self.image.draw(self.getImage())
        else :
            self.image_data_operator.getContour()
            self.image_data_operator.setImage(self.getImage())
            self.image_data_operator.recalculateArea(self.anchor.x, self.anchor.y, self.hu.low(), self.hu.high())
            self.image.draw(self.image_data_operator.getLabeled())

    def clickme(self):
        self.image.setPixmap(QPixmap(r"E:\muse\models\truck.jpg"))
        self.button.setText("huy")
        self.update()

    def UiComponents(self):
        vbox = QVBoxLayout(self)

        self.title = self._GetTitle()
        vbox.addWidget(QLabel(self.title))

        self.image = Render2d.WindowX(self.getImage(), self.setNewAnchorPoint, self.resetAnchorPoint)
        vbox.addWidget(self.image)

        vbox.addWidget(self.slider)

        self.setLayout(vbox)


