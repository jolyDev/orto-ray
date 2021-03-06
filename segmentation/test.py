import matplotlib.pyplot as plt
import numpy as np
import SimpleITK
from matplotlib.widgets import Slider

import mpl_interactions.ipyplot as iplt

x = np.linspace(0, np.pi, 200)
y = np.linspace(0, 10, 200)
X, Y = np.meshgrid(x, y)


pathDicom = "./data/head/"

reader = SimpleITK.ImageSeriesReader()
filenamesDICOM = reader.GetGDCMSeriesFileNames(pathDicom)
reader.SetFileNames(filenamesDICOM)
imgOriginal = reader.Execute()

def f(param1, param2):
    return SimpleITK.GetArrayFromImage(imgOriginal[:, :, 50])

fig, ax = plt.subplots()
controls = iplt.imshow(f, param1=(-5, 5), param2=(-3, 12))

plt.show()