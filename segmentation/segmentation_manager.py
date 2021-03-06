import SimpleITK

class SegmentationManager():
    def __init__(self, dicom_location):
        super().__init__()

        # init data
        reader = SimpleITK.ImageSeriesReader()
        reader.SetFileNames(reader.GetGDCMSeriesFileNames(dicom_location))
        self.data = reader.Execute()

        self.label_id = 1

    def getSliceYZ(self, index):
        return SimpleITK.GetArrayFromImage(self.data[index, :, :])

    def getSliceXZ(self, index):
        return SimpleITK.GetArrayFromImage(self.data[:, index, :])

    def getSliceXY(self, index):
        return SimpleITK.GetArrayFromImage(self.data[:, :, index])


    def labeSlice(self, slice_image, center_x: int, center_y: int, hu_min: int, hu_max: int):

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
        return SimpleITK.GetArrayFromImage(SimpleITK.LabelOverlay(image_smooth_binary, image_holes_erased))

