import os
import pydicom
import pydicom.uid
import numpy as np
import scipy
import scipy.ndimage
import cupyx.scipy.ndimage
import cupy as cp
from Core.Projection import View
from Core.Projection import view_to_int
import Algorithms.Trim
import SimpleITK

def getSlice(data, index: int, view: View):
    if view is View.FRONTAL and data.shape[0] >= index:
        return data[index, :, :]
    elif view is View.PROFILE and data.shape[1] >= index:
        return data[:, index, :]
    elif view is View.HORIZONTAL and data.shape[2] >= index:
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
        self.updateBounds()

    def updateBounds(self):
        shape = self.modified.shape
        self.x_max = shape[0] - 1
        self.x_min = 0
        self.y_max = shape[1] - 1
        self.y_min = 0
        self.z_max = shape[2] - 1
        self.z_min = 0

    def subscribe(self, listener):
        self.listeners.append(listener)

    def _dataChanged(self):
        self.updateBounds()
        for subscriber in self.listeners:
            subscriber.on3DDataChanged()

    def getMax(self, view: View):
        return self.origin.shape[view_to_int(view)]

    def getMaxModified(self, view: View):
        return self.modified.shape[view_to_int(view)]

    def getSlice(self, index: int, view: View):
        return getSlice(self.modified, index, view)

    def get(self):
        return self.origin

    def trim(self, x_max, x_min, y_max, y_min, z_max, z_min):
        self.x_max = int(x_max)
        self.x_min = int(x_min)
        self.y_max = int(y_max)
        self.y_min = int(y_min)
        self.z_max = int(z_max)
        self.z_min = int(z_min)

        self.modified = Algorithms.Trim.Trim(self.origin, self.x_max, self.x_min, self.y_max, self.y_min, self.z_max, self.z_min)
        self._dataChanged()
        return self.modified

    def rotate(self, angles):
        init_min = self.origin.min()
        init_max = self.origin.max()

        # rotate around x axis
        x = angles[0] - self.rotation.x
        self.rotation.x = x
        data_gpu = cp.asarray(self.modified)
        rotated = cupyx.scipy.ndimage.rotate(data_gpu, x, (1, 2), order=1)

        # rotate around y axis
        y = angles[1] - self.rotation.y
        self.rotation.y = y
        rotated = cupyx.scipy.ndimage.rotate(rotated, y, (0, 2), order=1)

        # rotate around z axis
        z = angles[2] - self.rotation.z
        self.rotation.z = z
        rotated = cupyx.scipy.ndimage.rotate(rotated, z, (0, 1), order=1)
        self.modified = np.clip(cp.asnumpy(rotated), init_min, init_max)

        self.x_min = int(0)
        self.y_min = int(0)
        self.z_min = int(0)

        self._dataChanged()

    def getOrigin(self):
        return self.origin

    def resetModification(self):
        self.modified = self.getOriginDeepCopy()
        self._dataChanged()

    def getOriginDeepCopy(self):
        return np.copy(self.origin)

    def getModified(self):
        return self.modified

    def setNewData(self, new_origin):
        self.origin = new_origin
        self.modified = self.getOriginDeepCopy()
        self._dataChanged()

    def denoise(self, data):
        itk_data = SimpleITK.GetImageFromArray(data)
        itk_data = SimpleITK.CurvatureFlow(itk_data, 0.125, 5)
        itk_data = SimpleITK.VotingBinaryHoleFilling(image1=itk_data)
                                          #majorityThreshold=1,
                                          #backgroundValue=0,
                                          #foregroundValue=labelWhiteMatter)
        return np.array(SimpleITK.GetArrayFromImage(itk_data), dtype=np.int64)
        #data = scipy.ndimage.uniform_filter(data, size=1)
        #data = scipy.ndimage.gaussian_filter(data, sigma=1)
        #return data

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

            self.origin = self.denoise(np.array(self.origin, dtype=np.int64))
            self.modified = self.getOriginDeepCopy()
            self._dataChanged()
        except Exception:
            self.origin = old_data
            self.modified = old_data
