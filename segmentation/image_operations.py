import SimpleITK


class ImageMutator():

    def __init__(self):
        self.label_id = 1
        self.image = None

    def getLabeled(self):
        return (SimpleITK.GetArrayFromImage(self.labled))

    def getArea(self):
        none_zero_pixels = self.mask[self.mask > 0]
        area = len(none_zero_pixels)
        print(area)
        return area

    def getContour(self):
        return -1

    def setImage(self, image):
        self.image = SimpleITK.GetImageFromArray(image)

    def recalculateArea(self, center_x: int, center_y: int, hu_min: int, hu_max: int):
        self.smooth = SimpleITK.CurvatureFlow(image1=self.image, timeStep=0.125, numberOfIterations=5)
        self.segmented = SimpleITK.ConnectedThreshold(image1=self.smooth,
                                                      seedList=[(int(center_x), int(center_y))],
                                                      lower=hu_min,
                                                      upper=hu_max,
                                                      replaceValue=self.label_id)

        self.mask = SimpleITK.Cast(SimpleITK.RescaleIntensity(self.smooth), self.segmented.GetPixelID())

        self.segmented_smooth = SimpleITK.VotingBinaryHoleFilling(image1=self.segmented,
                                                                  radius=[2] * 3,
                                                                  majorityThreshold=1,
                                                                  backgroundValue=0,
                                                                  foregroundValue=self.label_id)
        self.labled = SimpleITK.LabelOverlay(self.mask, self.segmented_smooth)
