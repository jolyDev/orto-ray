import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pyvi

from slice import SliceView, View
from segmentation.region_growing_manager import getImages

class Window(QWidget):

    def __init__(self):
        super().__init__()

        img = getImages()
        self.frontal_view = SliceView(self, View.FRONTAL, img)
        self.profile_view = SliceView(self, View.PROFILE, img)
        self.horizontal_view = SliceView(self, View.HORIZONTAL, img)
        #self.model = SliceView(self, "model", r'C:\athena.jpg')
        # setting title
        self.setWindowTitle("Ortho ray ")
        self.UiComponents()

        # showing all the widgets
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
