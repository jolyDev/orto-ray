from Algorithms.regionGrowthPlanes import segmentatePlanes
from Core.Projection import View
from Core.Projection import point2d
from Core.anchor_points import getRaw2D
from Core.DicomDataManager import getSlice

import  numpy as np

class Segmentation2DManager():
    def __init__(self):
        self.dicom = None
        self.anchors = None
        self.hu = None

        self.frontal_view = None
        self.profile_view = None
        self.horizontal_view = None

    def post_init(self, dicom, anchors, hu, frontal_view, profile_view, horizontal_view):
        self.dicom = dicom
        self.anchors = anchors
        self.hu = hu

        self.frontal_view = frontal_view
        self.profile_view = profile_view
        self.horizontal_view = horizontal_view

    def subscribe(self, slice_view):
        self.slice_view_listeners.append(slice_view)

    def update(self):
        if not self.anchors.anchors:
            self.frontal_view.resetImage()
            self.profile_view.resetImage()
            self.horizontal_view.resetImage()
            return

        hu_max = self.hu.slider.getMax()
        hu_min = self.hu.slider.getMin()
        seeds = self.anchors.getRaw3D()

        index_x = self.frontal_view.slider.getIndex()
        index_y = self.profile_view.slider.getIndex()
        index_z = self.horizontal_view.slider.getIndex()
        joint = np.array([index_x, index_y, index_z], dtype=np.int64)

        mask3d = segmentatePlanes(self.dicom.get(), joint, seeds, hu_max, hu_min)

        mask_x = getSlice(mask3d, index_x, self.frontal_view.view)
        mask_y = getSlice(mask3d, index_y, self.profile_view.view)
        mask_z = getSlice(mask3d, index_z, self.horizontal_view.view)

        self.frontal_view.overlay(mask_x)
        self.profile_view.overlay(mask_y)
        self.horizontal_view.overlay(mask_z)




