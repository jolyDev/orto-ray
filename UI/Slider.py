from PyQt5.QtWidgets import (QWidget, QSlider, QHBoxLayout,
                             QLabel, QApplication)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys


class Slider(QWidget):

    def __init__(self, parent, min, max, callback):
        super().__init__()

        self.parent = parent
        self.callback = callback
        self.index = int((max - min ) / 2)

        hbox = QHBoxLayout()

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(min, max - 1)
        self.slider.setValue(self.index)
        self.slider.setFocusPolicy(Qt.NoFocus)
        self.slider.setPageStep(1)

        self.slider.valueChanged.connect(self.onDataChanged)

        self.label = QLabel(str(min), self)
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.label.setMinimumWidth(80)
        self.label.setText(str(self.index))

        hbox.addWidget(self.slider)
        hbox.addSpacing(15)
        hbox.addWidget(self.label)

        self.setLayout(hbox)

    def onDataChanged(self, value):
        self.index = value
        self.label.setText(str(value))
        self.callback()

    def setRange(self, min, max):
        if min > self.slider.value():
            self.index = min

        if max < self.slider.value():
            self.index = max

        self.slider.setValue(self.index)
        self.onDataChanged(self.index)
        self.slider.setRange(min, max - 1)

    def getIndex(self):
        return self.index