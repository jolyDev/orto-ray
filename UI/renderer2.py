import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pyvi

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class WindowX(QMainWindow):
    def __init__(self, data):
        super().__init__()

        title = "Matplotlib Embeding In PyQt5"
        top = 400
        left = 400
        width = 900
        height = 500

        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)
        self.data = data
        self.MyUI()

    def MyUI(self):
        canvas = Canvas(self.data, self, width=8, height=4)
        canvas.move(0, 0)

class Canvas(FigureCanvas):
    def __init__(self, data ,parent=None, width=5, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.data = data
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        self.plot()

    def plot(self):
        self.axes.clear()

        # plot data
        self.axes.imshow(self.data)

        self.draw()