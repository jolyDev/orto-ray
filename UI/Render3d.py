import sys

# Setting the Qt bindings for QtPy
import os
os.environ["QT_API"] = "pyqt5"

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow

import numpy as np

import pyvista as pv
from pyvistaqt import QtInteractor

import Style as styling
class Render3D(QMainWindow):

    def __init__(self, data, parent=None, show=True):
        QtWidgets.QMainWindow.__init__(self, parent)

        # create the frame
        self.frame = QtWidgets.QFrame()
        vlayout = QtWidgets.QVBoxLayout()

        # add the pyvista interactor object
        self.plotter = QtInteractor(self.frame)
        vlayout.addWidget(self.plotter.interactor)

        self.frame.setLayout(vlayout)
        self.setCentralWidget(self.frame)

        self.update(data)

    def update(self, data):
        self.plotter.clear()
        self.plotter.add_bounding_box()
        self.plotter.add_volume(data, cmap=styling._COLOR_STYLE)
        self.show()