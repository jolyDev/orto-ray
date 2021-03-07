import SimpleITK
import matplotlib.pyplot as plt

class SegmentationManager():
    def __init__(self, dicom_location):
        super().__init__()

        # init data
        reader = SimpleITK.ImageSeriesReader()
        reader.SetFileNames(reader.GetGDCMSeriesFileNames(dicom_location))
        self.data = reader.Execute()

        self.label_id = 1
        plt.set_cmap("gray")

    def getSliceYZ(self, index):
        return SimpleITK.GetArrayFromImage(self.data[index, :, :])

    def getSliceXZ(self, index):
        return SimpleITK.GetArrayFromImage(self.data[:, index, :])

    def getSliceXY(self, index):
        return SimpleITK.GetArrayFromImage(self.data[:, :, index])

    def getMaxX(self):
        return SimpleITK.GetArrayFromImage(self.data).shape[2]

    def getMaxY(self):
        return SimpleITK.GetArrayFromImage(self.data).shape[1]

    def getMaxZ(self):
        return SimpleITK.GetArrayFromImage(self.data).shape[0]