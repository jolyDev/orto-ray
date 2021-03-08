import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pyvi

from Slice import SliceView, View
from hu_manager import HounsfieldUnitsManager
from segmentation.segmentation_manager import SegmentationManager
from MultiSelection.AnchorPoints import AnchorPointsManager

class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.anchor_manager = AnchorPointsManager()

        self.dicom_manager = SegmentationManager("E:/orto-ray/dicom_data/head")
        self.frontal_view = SliceView(self, View.FRONTAL, self.dicom_manager, self.anchor_manager.apply, self.anchor_manager.reset)
        self.profile_view = SliceView(self, View.PROFILE, self.dicom_manager, self.anchor_manager.apply, self.anchor_manager.reset)
        self.horizontal_view = SliceView(self, View.HORIZONTAL, self.dicom_manager, self.anchor_manager.apply, self.anchor_manager.reset)

        self.anchor_manager.addListener(self.frontal_view)
        self.anchor_manager.addListener(self.profile_view)
        self.anchor_manager.addListener(self.horizontal_view)

        #self.model = SliceView(self, "model", r'C:\athena.jpg')
        self.setWindowTitle("Ortho Ray")
        self.UiComponents()

        self.show()

    def updateLabeling(self, min, max):
        self.frontal_view.updateLabelImage(min, max)
        self.profile_view.updateLabelImage(min, max)
        self.horizontal_view.updateLabelImage(min, max)

    def UiComponents(self):
        hbox = QHBoxLayout(self)

        grid = QGridLayout(self)

        grid.addWidget(self.horizontal_view,0,0)
        grid.addWidget(QWidget(),0,1)
        grid.addWidget(self.profile_view,1,0)
        grid.addWidget(self.frontal_view,1,1)

        hbox.addLayout(grid)
        hbox.addWidget(HounsfieldUnitsManager(self.anchor_manager.onHU_BoundsChanged))
        self.showMaximized()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
