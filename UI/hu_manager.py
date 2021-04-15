
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

from SliderX import SliderX


class HounsfieldUnitsManager(QWidget):

    def __init__(self, callback):
        super(HounsfieldUnitsManager, self).__init__()

        default = 1000

        self.callback = callback
        vbox = QVBoxLayout(self)

        hbox_max = QHBoxLayout(self)
        hbox_max.addWidget(QLabel("max"))
        self.max = QSpinBox(self)
        self.max.setMaximum(2 * default)
        self.max.setMinimum(-default)
        self.max.setValue(default)
        self.max.valueChanged.connect(self.boundsChanged)
        hbox_max.addWidget(self.max)
        vbox.addLayout(hbox_max)

        self.slider = SliderX(-default, default, self.callback, False)
        self.slider.slider.setLow(- default / 4)
        self.slider.slider.setHigh( default / 4)
        vbox.addWidget(self.slider)
        hbox_min = QHBoxLayout(self)
        hbox_min.addWidget(QLabel("min"))
        self.min = QSpinBox(self)
        self.min.setMaximum(2 * default)
        self.min.setMinimum(-default)
        self.min.setValue(-default)
        self.min.valueChanged.connect(self.boundsChanged)
        hbox_min.addWidget(self.min)
        vbox.addLayout(hbox_min)

    def boundsChanged(self, value):
        self.slider.setMinBound(int(self.min.value()))
        self.slider.setMaxBound(int(self.max.value()))
        self.dataChanged()
