import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pyvi

from Slice import SliceView, View
from Slider2 import RangeSliderHU
from segmentation.segmentation_manager import SegmentationManager

class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.dicom_manager = SegmentationManager("E:/orto-ray/dicom_data/head")
        self.hu = RangeSliderHU("hu", 15, 35, 0, 255, self.update)
        self.frontal_view = SliceView(self, View.FRONTAL, self.dicom_manager, self.hu)
        self.profile_view = SliceView(self, View.PROFILE, self.dicom_manager, self.hu)
        self.horizontal_view = SliceView(self, View.HORIZONTAL, self.dicom_manager, self.hu)
        #self.model = SliceView(self, "model", r'C:\athena.jpg')
        self.setWindowTitle("Ortho Ray")
        self.UiComponents()

        self.show()

    def update(self):
        self.frontal_view.update()
        self.profile_view.update()
        self.horizontal_view.update()

    def UiComponents(self):
        hbox = QHBoxLayout(self)

        grid = QGridLayout(self)

        grid.addWidget(self.horizontal_view,0,0)
        grid.addWidget(QWidget(),0,1)
        grid.addWidget(self.profile_view,1,0)
        grid.addWidget(self.frontal_view,1,1)

        hbox.addLayout(grid)
        hbox.addWidget(self.hu)
        self.showMaximized()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
