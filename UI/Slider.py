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
        self.index = min

        hbox = QHBoxLayout()

        sld = QSlider(Qt.Horizontal, self)
        sld.setRange(min, max - 1)
        sld.setValue(70)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setPageStep(1)

        sld.valueChanged.connect(self.onDataChanged)

        self.value = sld

        self.label = QLabel(str(min), self)
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.label.setMinimumWidth(80)

        hbox.addWidget(sld)
        hbox.addSpacing(15)
        hbox.addWidget(self.label)

        self.setLayout(hbox)

    def onDataChanged(self, value):
        self.index = value
        self.label.setText(str(value))
        self.callback()

    def getIndex(self):
        return self.index