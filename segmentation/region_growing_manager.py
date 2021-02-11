import mpl_interactions.ipyplot as iplt
import ipywidgets as widgets
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider
from mpl_interactions import interactive_plot
import SimpleITK
from mpl_interactions import ioff, panhandler, zoom_factory
import numpy as np

dicom_dir = "C://"

FRONT = "front"
SIDE = "side"
TOP = "top"

view = np.linspace(0, 2, 3)

slice = np.linspace(0, 200, 201)

x = np.linspace(0, 250, 251)
y = np.linspace(0, 250, 251)

coords = []

lover = np.linspace(-1000, 1000, 10000)
upper = np.linspace(-1000, 1000, 10000)

style = ['fivethirtyeight',
 'seaborn-pastel',
 'seaborn-whitegrid',
 'ggplot',
 'grayscale']


labelWhiteMatter = 1
labelGrayMatter = 2

def onclick(event):
    global ix, iy
    ix, iy = event.xdata, event.ydata

    global coords
    coords.append((ix, iy))

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x, y)

    if len(coords) == 2:
        fig.canvas.mpl_disconnect(cid)

    return coords

cid = plt.figure().canvas.mpl_connect('button_press_event', onclick)

pathDicom = "E:/orto-ray/dicom_data/head"

reader = SimpleITK.ImageSeriesReader()
filenamesDICOM = reader.GetGDCMSeriesFileNames(pathDicom)
reader.SetFileNames(filenamesDICOM)
imgOriginal = reader.Execute()


def sitk_show(img, title=None, margin=0.05, dpi=40):
    nda = SimpleITK.GetArrayFromImage(img)
    spacing = img.GetSpacing()
    figsize = (1 + margin) * nda.shape[0] / dpi, (1 + margin) * nda.shape[1] / dpi
    extent = (0, nda.shape[1] * spacing[1], nda.shape[0] * spacing[0], 0)
    fig = plt.figure(figsize=figsize, dpi=dpi)
    ax = fig.add_axes([margin, margin, 1 - 2 * margin, 1 - 2 * margin])

    plt.set_cmap("gray")
    ax.imshow(nda, extent=extent, interpolation=None)

    if title:
        plt.title(title)

    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed') #works fine on Windows!


def label_area(center_x: int, center_y: int, hu_min: int, hu_max: int, slice:int, view):
    img2d = ""
    if view == 0:
        img2d = imgOriginal[int(slice), :, :]
    if view == 1:
        img2d = imgOriginal[:, int(slice), :]
    if view == 2:
        img2d = imgOriginal[:, :, int(slice)]

    img2dSmooth = SimpleITK.CurvatureFlow(image1=img2d, timeStep=0.125, numberOfIterations=5)

    print(center_x.real)

    imgWhiteMatter = SimpleITK.ConnectedThreshold(image1=img2dSmooth,
                                                  seedList=[(int(center_x), int(center_y))],
                                                  lower=hu_min,
                                                  upper=hu_max,
                                                  replaceValue=labelWhiteMatter)

    # Rescale 'imgSmooth' and cast it to an integer type to match that of 'imgWhiteMatter'
    imgSmoothInt = SimpleITK.Cast(SimpleITK.RescaleIntensity(img2dSmooth), imgWhiteMatter.GetPixelID())

# Use 'LabelOverlay' to overlay 'imgSmooth' and 'imgWhiteMatter'

    imgWhiteMatterNoHoles = SimpleITK.VotingBinaryHoleFilling(image1=imgWhiteMatter,
                                                              radius=[2]*3,
                                                              majorityThreshold=1,
                                                              backgroundValue=0,
                                                              foregroundValue=labelWhiteMatter)
    return SimpleITK.GetArrayFromImage(SimpleITK.LabelOverlay(imgSmoothInt, imgWhiteMatterNoHoles))

controls = iplt.imshow(label_area, center_x=x, center_y=y, hu_min = lover, hu_max = upper, slice = slice, view = view)

plt.set_cmap("gray")
plt.show()