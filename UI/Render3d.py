import sys

# Setting the Qt bindings for QtPy
import os
os.environ["QT_API"] = "pyqt5"

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QRadioButton

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
        self.plotter.set_background("royalblue", top="aliceblue")
        vlayout.addWidget(self.plotter.interactor)

        self.frame.setLayout(vlayout)
        self.setCentralWidget(self.frame)

        self.update3D(data)

    def update3D(self, data):
        self.plotter.clear()
        self.plotter.add_bounding_box()
        self.plotter.add_volume(data, cmap="gray")
        self.show()

    def updateSlice(self, data):
        self.plotter.clear()
        self.plotter.add_bounding_box()
        opacity = [0, 0.1, 0.1, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        self.plotter.add_volume(data, cmap="gray", opacity=opacity)
        self.show()