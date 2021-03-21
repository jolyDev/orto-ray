import SimpleITK
import matplotlib.pyplot as plt

from common.ProjectionTypes import View
from common.ProjectionTypes import viewToInt

from Utilities import logger

class SegmentationManager():
    def __init__(self, dicom_location):
        super().__init__()

        # init data
        reader = SimpleITK.ImageSeriesReader()
        reader.SetFileNames(reader.GetGDCMSeriesFileNames(dicom_location))
        self.data = reader.Execute()

        self.label_id = 1
        plt.set_cmap("gray")

    def getData(self):
        return SimpleITK.GetArrayFromImage(self.data)

    def getSlice(self, index, view : View):
        if view is View.FRONTAL:
            return SimpleITK.GetArrayFromImage(self.data[index, :, :])
        elif view is View.PROFILE:
            return SimpleITK.GetArrayFromImage(self.data[:, index, :])
        elif view is View.HORIZONTAL:
            return SimpleITK.GetArrayFromImage(self.data[:, :, index])
        else:
            assert False

    def getMax(self, view : View):
        return SimpleITK.GetArrayFromImage(self.data).shape[2 - viewToInt(view)] # inverted

    def getArea(self):
        return self.area

    def getDimetionsSize(self):
        return self.data.GetSpacing()

    def calculateArea(self, image, single_pixel_area):
        numpy_array = SimpleITK.GetArrayFromImage(image)

        filter_arr = numpy_array != 0

        newarr = numpy_array[filter_arr]
        none_zero_pixels = numpy_array[newarr]
        self.area = len(none_zero_pixels) * single_pixel_area
        print(self.area)


    def labeSlice(self, slice_image, center_x: int, center_y: int, hu_min: int, hu_max: int, single_pixel_area):

        image = SimpleITK.GetImageFromArray(slice_image)
        smooth_image = SimpleITK.CurvatureFlow(image1=image, timeStep=0.125, numberOfIterations=5)

        filtered_data = SimpleITK.ConnectedThreshold(image1=smooth_image,
                                                     seedList=[(int(center_x), int(center_y))],
                                                     lower=hu_min,
                                                     upper=hu_max,
                                                     replaceValue=self.label_id)

        # Rescale 'imgSmooth' and cast it to an integer type to match that of 'imgWhiteMatter'
        image_smooth_binary = SimpleITK.Cast(SimpleITK.RescaleIntensity(smooth_image), filtered_data.GetPixelID())

        # Use 'LabelOverlay' to overlay 'imgSmooth' and 'imgWhiteMatter'

        image_holes_erased = SimpleITK.VotingBinaryHoleFilling(image1=filtered_data,
                                                               radius=[2]*3,
                                                               majorityThreshold=1,
                                                               backgroundValue=0,
                                                               foregroundValue=self.label_id)
        self.calculateArea(filtered_data, single_pixel_area)
        return SimpleITK.GetArrayFromImage(SimpleITK.LabelOverlay(image_smooth_binary, image_holes_erased))

