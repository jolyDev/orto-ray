import os
import pydicom
import pydicom.uid
import numpy as np
import scipy.ndimage
from Core.Projection import View
from Core.Projection import view_to_int

class DicomDataManager():
    def __init__(self, dicom_rooth_path):
        self.listeners = []
        self.origin = []
        self.loadDicom(dicom_rooth_path)

    def subscribe(self, listener):
        self.listeners.append(listener)

    def _dataChanged(self):
        for subscriber in self.listeners:
            subscriber.on3DDataChanged(self.modified)

    def getMax(self, view: View):
        return self.origin.shape[view_to_int(view)]

    def getSlice(self, index: int, view: View):
        if view is View.FRONTAL:
            return self.origin[index, :, :]
        elif view is View.PROFILE:
            return self.origin[:, index, :]
        elif view is View.HORIZONTAL:
            return self.origin[:, :, index]

    def get(self):
        return self.origin

    def getOrigin(self):
        return self.origin

    def getOriginDeepCopy(self):
        return np.copy(self.origin)

    def getModified(self):
        return self.modified

    def setNewData(self, new_origin):
        self.origin = new_origin
        self.modified = self.getOriginDeepCopy()
        self._dataChanged()

    def loadDicom(self, dicom_rooth_path):
        old_data = self.getOriginDeepCopy()
        try:
            slices = [pydicom.read_file(dicom_rooth_path + '/' + s) for s in os.listdir(dicom_rooth_path)]
            slices.sort(key=lambda x: int(x.InstanceNumber))

            # pixel aspects, assuming all slices are the same
            ps = slices[0].PixelSpacing
            ss = slices[0].SliceThickness
            ax_aspect = ps[1] / ps[0]
            sag_aspect = ps[1] / ss
            cor_aspect = ss / ps[0]

            # create 3D array
            img_shape = list(slices[0].pixel_array.shape)
            img_shape.append(len(slices))
            self.origin = np.zeros(img_shape)
            self.modified = self.getOriginDeepCopy()

            # fill 3D array with the images from the files
            for i, s in enumerate(slices):
                img2d = s.pixel_array
                self.origin[:, :, i] = np.array(img2d, dtype=np.int64)

            self.origin = np.array(self.origin, dtype=np.int64)
            self._dataChanged()
        except Exception:
            self.origin = old_data
            self.modified = old_data
