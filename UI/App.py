import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pyvi

from Slice import SliceView, View
from segmentation.segmentation_manager import SegmentationManager

class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.dicom_manager = SegmentationManager("E:/orto-ray/dicom_data/head")
        self.frontal_view = SliceView(self, View.FRONTAL, self.dicom_manager)
        self.profile_view = SliceView(self, View.PROFILE, self.dicom_manager)
        self.horizontal_view = SliceView(self, View.HORIZONTAL, self.dicom_manager)
        #self.model = SliceView(self, "model", r'C:\athena.jpg')
        self.setWindowTitle("Ortho Ray")
        self.UiComponents()

        self.show()


    def UiComponents(self):
        grid = QGridLayout(self)

        grid.addWidget(self.frontal_view,0,0)
        grid.addWidget(QWidget(),0,1)
        grid.addWidget(self.profile_view,1,0)
        grid.addWidget(self.horizontal_view,1,1)

        self.showMaximized()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
