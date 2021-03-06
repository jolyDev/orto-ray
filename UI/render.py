from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtOpenGL import QGLWidget
import sys
import vtk
from vtk import *
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class vtkMW(QMainWindow):
    """docstring for Mainwindow"""

    def __init__(self, parent=None):
        super(vtkMW, self).__init__(parent)
        self.basic()
        vll = self.kuangti()
        self.setCentralWidget(vll)

    # Window Basic Properties
    def basic(self):
        # Set title, size, icon
        self.setWindowTitle("GT1")
        self.resize(1100, 650)
        self.setWindowIcon(QIcon("./image/Gt1.png"))

    def kuangti(self):
        frame = QFrame()
        vl = QVBoxLayout()
        vtkWidget = QVTKRenderWindowInteractor()
        vl.addWidget(vtkWidget)
        # vl.setContentsMargins(0,0,0,0)
        ren = vtk.vtkRenderer()
        ren.SetBackground(0.01, 0.2, 0.01)
        # renderer.GetActiveCamera().SetPosition() #Set the viewpoint position
        # renderer.GetActiveCamera().SetViewUp(0, 1, 0) #Set the view direction
        vtkWidget.GetRenderWindow().AddRenderer(ren)
        self.iren = vtkWidget.GetRenderWindow().GetInteractor()
        self.Creatobj(ren)
        self.iren.Initialize()
        frame.setLayout(vl)
        return frame

    def Creatobj(self, ren):
        # Create source
        filename = r"E:\muse\models\face.obj"
        reader = vtk.vtkOBJReader()
        reader.SetFileName(filename)
        reader.Update()

        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())

        # Create an actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        ren.AddActor(actor)
        ren.ResetCamera()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = vtkMW()
    win.show()
    # win.iren.Initialize()
    sys.exit(app.exec_())