from enum import Enum

class View(Enum):
    FRONTAL = 0
    PROFILE = 1
    HORIZONTAL = 2

def viewToInt(view : View):
    if view is View.FRONTAL:
        return 0
    elif view is View.PROFILE:
        return 1
    elif view is View.HORIZONTAL:
        return 2
    return -1