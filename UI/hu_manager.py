
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

from SliderX import SliderX


class HounsfieldUnitsManager(QWidget):

    def __init__(self, max_hu, min_hu, callback):
        super(HounsfieldUnitsManager, self).__init__()

        default = 1000

        self.callback = callback
        vbox = QVBoxLayout(self)

        hbox_max = QHBoxLayout(self)
        hbox_max.addWidget(QLabel("max"))
        self.max = QSpinBox(self)
        self.max.setMaximum(max_hu)
        self.max.setMinimum(min_hu)
        self.max.setValue(max_hu)
        self.max.valueChanged.connect(self.boundsChanged)
        hbox_max.addWidget(self.max)
        vbox.addLayout(hbox_max)

        self.slider = SliderX(min_hu, max_hu, self.callback, False)
        self.slider.slider.setHigh(int((max_hu - min_hu) * 0.75))
        self.slider.slider.setLow(int((max_hu - min_hu) * 0.25))
        vbox.addWidget(self.slider)
        hbox_min = QHBoxLayout(self)
        hbox_min.addWidget(QLabel("min"))
        self.min = QSpinBox(self)
        self.min.setMaximum(max_hu)
        self.min.setMinimum(min_hu)
        self.min.setValue(min_hu)
        self.min.valueChanged.connect(self.boundsChanged)
        hbox_min.addWidget(self.min)
        vbox.addLayout(hbox_min)

    def boundsChanged(self, value):
        self.slider.setMinBound(int(self.min.value()))
        self.slider.setMaxBound(int(self.max.value()))
        self.dataChanged()
