import os
import pydicom
import pydicom.uid
import numpy as np
import scipy.ndimage
#import cupyx.scipy.ndimage
from Core.Projection import View
from Core.Projection import view_to_int
import Algorithms.Trim

def getSlice(data, index: int, view: View):
    if view is View.FRONTAL:
        return data[index, :, :]
    elif view is View.PROFILE:
        return data[:, index, :]
    elif view is View.HORIZONTAL:
        return data[:, :, index]

class DicomDataManager():
    class Rotation:
        x: float = 0.0
        y: float = 0.0
        z: float = 0.0

    def __init__(self, dicom_rooth_path):
        self.listeners = []
        self.origin = []
        self.loadDicom(dicom_rooth_path)
        self.rotation = DicomDataManager.Rotation()

    def subscribe(self, listener):
        self.listeners.append(listener)

    def _dataChanged(self):
        for subscriber in self.listeners:
            subscriber.on3DDataChanged(self.modified)

    def getMax(self, view: View):
        return self.origin.shape[view_to_int(view)]

    def getMaxModified(self, view: View):
        return self.modified.shape[view_to_int(view)]

    def getSlice(self, index: int, view: View):
        return getSlice(self.origin, index, view)

    def get(self):
        return self.origin

    def trim(self, x_max, x_min, y_max, y_min, z_max, z_min):
        x_max = int(x_max)
        x_min = int(x_min)
        y_max = int(y_max)
        y_min = int(y_min)
        z_max = int(z_max)
        z_min = int(z_min)

        curr_shape = self.modified.shape
        if (curr_shape[0] == x_max - x_min and
            curr_shape[1] == y_max - y_min and
            curr_shape[2] == z_max - z_min):
            return self.modified

        if (curr_shape[0] > x_max - x_min and
            curr_shape[1] > y_max - y_min and
            curr_shape[2] > z_max - z_min):
            self.modified = Algorithms.Trim.Trim(self.modified, x_max, x_min, y_max, y_min, z_max, z_min)
        else:
            self.modified = Algorithms.Trim.Trim(self.origin, x_max, x_min, y_max, y_min, z_max, z_min)

        return self.modified

    def getRotated(self, angles):
        init_min = self.origin.min()
        init_max = self.origin.max()

        # rotate around x axis
        x = angles[0] - self.rotation.x
        self.rotation.x = x
        self.modified = scipy.ndimage.interpolation.rotate(self.modified, x, (1, 2))

        # rotate around y axis
        y = angles[1] - self.rotation.y
        self.rotation.y = y
        self.modified = scipy.ndimage.interpolation.rotate(self.modified, y, (0, 2))

        # rotate around z axis
        z = angles[2] - self.rotation.z
        self.rotation.z = z
        self.modified = scipy.ndimage.interpolation.rotate(self.modified, z, (0, 1))

        return np.clip(self.modified, init_min, init_max)

    def getOrigin(self):
        return self.origin

    def resetModification(self):
        self.modified = self.getOriginDeepCopy()

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

            # fill 3D array with the images from the files
            for i, s in enumerate(slices):
                img2d = s.pixel_array
                self.origin[:, :, i] = np.array(img2d, dtype=np.int64)

            self.origin = np.array(self.origin, dtype=np.int64)
            self.modified = self.getOriginDeepCopy()
            self._dataChanged()
        except Exception:
            self.origin = old_data
            self.modified = old_data
