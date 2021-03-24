import pyvista as pv

def volume(data):
    dataX = pv.wrap(data)
    dataX.plot(volume=True, eye_dome_lighting=True, parallel_projection=True) # Volume render
