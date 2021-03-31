from enum import Enum
import numpy as np

class View(Enum):
    FRONTAL    = 0 # x
    PROFILE    = 1 # y
    HORIZONTAL = 2 # z

def view_to_int(view: View):
    if view is View.FRONTAL:
        return 0
    elif view is View.PROFILE:
        return 1
    elif view is View.HORIZONTAL:
        return 2
    return -1

def view_to_str(view: View) -> str:
    if view == View.FRONTAL:
        return "Frontal"
    if view == View.PROFILE:
        return "Profile"
    if view == View.HORIZONTAL:
        return "Horizontal"

class point2d():
    def __init__(self, x : int, y : int, view : View):
        self.x = x
        self.y = y
        self.view = view

    def to3d(self, index : int):
        if self.view == View.FRONTAL:
            return point3d(index, self.x, self.y)
        if self.view == View.PROFILE:
            return point3d(self.x, index, self.y)
        if self.view == View.HORIZONTAL:
            return point3d(self.x, self.y, index)

        return [-1, -1, -1]

class point3d():
    def __init__(self, x : int, y : int, z : int):
        self.x = x
        self.y = y
        self.z = z

    def get2d(self, view: View):
        if view == View.FRONTAL:
            return point2d(self.y, self.z, view)
        if view == View.PROFILE:
            return point2d(self.x, self.z, view)
        if view == View.HORIZONTAL:
            return point2d(self.x, self.y, view)

class plane():
    def __init__(self, data2d, view : View):
        self.data2d = data2d
        self.view = view

def toNumPy(data):
    return np.array(data, dtype=np.int64)