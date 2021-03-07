import sys
from enum import Enum

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pyvi
import numpy as np
from Slider import Slider
from PIL import Image

import renderer2

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

    def __init__(self, parent, view: View, data_manager):
        super().__init__()

        self.parent = parent
        self.view = view
        self.data_manager = data_manager
        self.slider = Slider(self, 0, self._GetSliderMax(), self.updateImage)
        self.title = self._GetTitle()

        self.image = renderer2.WindowX(self.getImage())
        # setting title
        self.UiComponents()

        # showing all the widgets
        self.show()

        # method for widgets

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

    def updateImage(self):
        self.image.draw(self.getImage())

    def clickme(self):
        self.image.setPixmap(QPixmap(r"E:\muse\models\truck.jpg"))
        self.button.setText("huy")
        self.update()

    def UiComponents(self):
        vbox = QVBoxLayout(self)

        vbox.addWidget(QLabel(self.title))
        vbox.addWidget(self.image)
        vbox.addWidget(self.slider)

        self.setLayout(vbox)


