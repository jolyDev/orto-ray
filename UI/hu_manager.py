
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

from Slider2 import RangeSliderHU


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

        self.slider = RangeSliderHU(- default / 4, default / 4, -default, default, self.dataChanged)

        self.upper = QLabel(str(self.slider.getMax()))
        vbox.addWidget(self.upper)

        vbox.addWidget(self.slider)

        self.lower = QLabel(str(self.slider.getMin()))
        vbox.addWidget(self.lower)

        hbox_min = QHBoxLayout(self)
        hbox_min.addWidget(QLabel("min"))
        self.min = QSpinBox(self)
        self.min.setMaximum(2 * default)
        self.min.setMinimum(-default)
        self.min.setValue(-default)
        self.min.valueChanged.connect(self.boundsChanged)
        hbox_min.addWidget(self.min)
        vbox.addLayout(hbox_min)


    def dataChanged(self):
        min = self.slider.getMin()
        max = self.slider.getMax()
        self.upper.setText(str(max))
        self.lower.setText(str(min))
        self.callback(min, max)

    def boundsChanged(self, value):
        self.slider.setMinBound(int(self.min.value()))
        self.slider.setMaxBound(int(self.max.value()))
        self.dataChanged()
