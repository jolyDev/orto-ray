import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pyvi

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class WindowX(QMainWindow):
    def __init__(self, data, apply, reset):
        super().__init__()

        title = "Matplotlib Embeding In PyQt5"

        self.setWindowTitle(title)
        self.data = data
        self.canvas = Canvas(self.data, self, width=8, height=4)
        self.canvas.move(0, 0)
        self.canvas.mpl_connect('button_press_event', self.onClick)

        self.apply = apply
        self.reset = reset

    def onClick(self, event):
        if not event.button == 1:
            self.reset()
        else:
            # swap data because on image it`s interpretated as row and columns
            # but client side treats it as x and y
            self.apply(event.ydata, event.xdata)

    def draw(self, data):
        self.canvas.plotX(data, [])

    def drawOverlayed(self, data, mask):
        self.canvas.data = data
        self.canvas.plotX(data, mask)

class Canvas(FigureCanvas):
    def __init__(self, data ,parent=None, width=5, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.data = data
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        self.overlay = False
        self.plot()

    def plot(self):
        self.axes.clear()

        # plot data
        self.axes.imshow(self.data)

        self.draw()

    def plotX(self, data, mask):
        self.axes.clear()

        # plot data
        self.axes.imshow(data)

        if len(mask):
            self.axes.imshow(mask, 'copper', alpha=0.5)

        self.draw()
