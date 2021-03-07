import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets
import RangeSlider

def echo(low_value, high_value):
	print(low_value, high_value)

def main(argv):
    app = QtWidgets.QApplication(sys.argv)
    slider = RangeSlider.RangeSliderHU("hu", 15, 35, 0, 255, echo)
    slider.show()
    slider.raise_()
    app.exec_()

if __name__ == "__main__":
    main(sys.argv)