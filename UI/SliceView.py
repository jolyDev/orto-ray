from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
from Slider import Slider
import matplotlib
import datetime
import os.path

from numpngw import write_png
from time import gmtime, strftime
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
        self.slider = Slider(self, 0, self.dicom.getMax(self.view), segmentation2d_callback, self.onMouseRelease)
        self.anchor_apply = apply_callback
        self.image = Render2d.Render2D(self.getImage(), self.apply, reset_callback)
        self.release_callback = None
        #self.pixel_area = self.getPixelArea(self.data_manager.getDimetionsSize())

        self.UiComponents()
        self.show()

    def apply(self, x, y):
        self.anchor_apply(self, x, y)

    def rotate(self, image):
        return np.rot90(image, 3)

    def _getName(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        if dlg.exec_():
            path = dlg.selectedFiles()
            return os.path.join(path[0], strftime("%a_%d_%b_%Y_%X", gmtime()).replace(":", "_"))

        return ""

    def saveOne(self):
        matplotlib.image.imsave(self._getName() + ".png", self.getImage())

    def saveAll(self):
        min, max = self.getMinBoundForView()
        name_template = self._getName()
        for i in range (max - min):
            image = self.dicom.getSlice(i - int(min), self.view)
            matplotlib.image.imsave(name_template + '_' + str(i) + '.jpg', image)

    def getMinBoundForView(self):
        if (self.view == View.FRONTAL):
            min = self.dicom.x_min
            max = self.dicom.x_max
        elif (self.view == View.PROFILE):
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

    def addReleaseCallback(self, release_callback):
        self.release_callback = release_callback

    def onMouseRelease(self):
        if self.release_callback is not None:
            self.release_callback()

    def overlay(self, mask):
        self.image.drawOverlayed(self.getImage(), mask)

    def UiComponents(self):
        vbox = QVBoxLayout(self)

        vbox.addWidget(QLabel(view_to_str(self.view)))

        vbox.addWidget(self.image)

        vbox.addWidget(self.slider)

        hbox = QHBoxLayout(self)
        save_one = QPushButton("Save one")
        save_one.clicked.connect(self.saveOne)

        save_all = QPushButton("Save all")
        save_all.clicked.connect(self.saveAll)

        hbox.addWidget(save_one)
        hbox.addWidget(save_all)
        vbox.addLayout(hbox)

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

