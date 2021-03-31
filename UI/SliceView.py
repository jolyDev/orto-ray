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


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

def toRaw(point):
    raw = [[]]

    return np.array([[int(point.x), int(point.y)]], dtype=np.int64)

class SliceView(QWidget):

    def __init__(self, parent, view: View, dicom, apply_callback, reset_callback):
        super().__init__()

        plt.set_cmap("gray")
        self.parent = parent
        self.view = view
        self.dicom = dicom
        self.slider = Slider(self, 0, self._GetSliderMax(), self.updateImage)
        #self.pixel_area = self.getPixelArea(self.data_manager.getDimetionsSize())

        self.UiComponents()

        self.apply = apply_callback
        self.reset = reset_callback

        # showing all the widgets
        self.show()

        # method for widgets

    def resetAnchorPoint(self):
        self.reset()

    def setNewAnchorPoint(self, x, y):
        self.apply(self, x, y)

    def rotate(self, image):
        return np.rot90(image, 3)

    def updateImage(self):
        self.image.draw(self.getImage())

    def updateSegmentation(self, anchor, min, max):
        if not anchor:
            self.updateImage()
        else:
            data = np.array(self.getImage(), dtype=np.int64)
            anchor2 = toRaw(anchor[0].get2d(self.view))

            #print("{} | {} : {}".format(coord_1, coord_2, data2d[int(coord_1)][int(coord_2)]))

            start = time.time()
            mask = Algorithms.regionGrowth2D.segmentate2d(data, anchor2, int(max), int(min))
            end = time.time()

            self.image.drawOverlayed(data, mask)
            end2 = time.time()
            print((end - start) / (end2 - end))

    def UiComponents(self):
        vbox = QVBoxLayout(self)

        vbox.addWidget(QLabel(view_to_str(self.view)))

        self.image = Render2d.WindowX(self.getImage(), self.setNewAnchorPoint, self.resetAnchorPoint)
        vbox.addWidget(self.image)

        vbox.addWidget(self.slider)

        self.setLayout(vbox)

    def getView(self):
        return self.view

    def getImage(self):
        return self.dicom.getSlice(self.slider.getIndex(), self.view)

    def getPixelArea(self, width):
        if self.view == View.FRONTAL:
            return width[1] * width[2]
        if self.view == View.HORIZONTAL:
            return width[0] * width[2]
        if self.view == View.PROFILE:
            return width[0] * width[1]

    def _GetSliderMax(self):
        return self.dicom.getMax(self.view)

