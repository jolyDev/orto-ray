import sys
from enum import Enum

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pyvi
import numpy as np
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

def _GetName(view) -> str:
    if view == View.FRONTAL:
        return "frontal"
    if view == View.PROFILE:
        return "profile"
    if view == View.FRONTAL:
        return "horizontal"


class SliceView(QWidget):

    def _Get2dSlice():
        if view == View.FRONTAL:
            return "frontal"
        if view == View.PROFILE:
            return "profile"
        if view == View.FRONTAL:
            return "horizontal"

    def __init__(self, parent, view: View, img_pack):
        super().__init__()

        self.parent = parent
        self.view = view
        self.image = self.getImage(img_pack)
        self.button = QPushButton("Button two")
        self.title = _GetName(self.view)
        # setting title
        self.UiComponents()

        # showing all the widgets
        self.show()

        # method for widgets

    def getImage(self, img_pack):
        label = QLabel(self.parent)

        plt.imshow(img_pack)
        img = plt.savefig('books_read.png')
        i = 20
        x = img_pack
        y = array_to_pixmap(x)
        label.setPixmap(QPixmap(img))
        return renderer2.WindowX(img_pack)

    def clickme(self):
        self.image.setPixmap(QPixmap(r"E:\muse\models\truck.jpg"))
        self.button.setText("huy")
        self.update()

    def UiComponents(self):
        vbox = QVBoxLayout(self)
        self.button.clicked.connect(self.clickme)

        vbox.addWidget(QLabel(self.title))
        vbox.addWidget(self.image)
        vbox.addWidget(self.button)

        # adding action to a button
        self.button.clicked.connect(self.clickme)


