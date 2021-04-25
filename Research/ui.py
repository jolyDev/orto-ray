import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QFileDialog, QAction
from PyQt5.QtGui import QIcon, QPixmap

class MainWindow(QMainWindow):

    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        editMenu = menubar.addMenu('Edit')
        self.resize(500, 500)

        dlg = QFileDialog(self)       
        openAction = QAction('Open Image', self)  
        openAction.triggered.connect(self.openImage) 
        fileMenu.addAction(openAction)

        closeAction = QAction('Exit', self)  
        closeAction.triggered.connect(self.close) 
        fileMenu.addAction(closeAction)



    def openImage(self):
    # This function is called when the user clicks File->Open Image.
        label = QLabel(self)
        filename = QFileDialog.getOpenFileName()
        imagePath = filename[0]
        print(imagePath)
        pixmap = QPixmap(imagePath)
        label.setPixmap(pixmap)
        self.resize(pixmap.width(),pixmap.height())
        self.show()



def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec_()

if __name__ == '__main__':
    sys.exit(main()) 