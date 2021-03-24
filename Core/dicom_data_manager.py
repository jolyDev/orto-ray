import os
import pydicom
import pydicom.uid
import numpy as np
import scipy.ndimage

class dicom_manager():
    def __init__(self, dicom_rooth_path):
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
        self.data3d = np.zeros(img_shape)

        # fill 3D array with the images from the files
        for i, s in enumerate(slices):
            img2d = s.pixel_array
            self.data3d[:, :, i] = img2d

        self.data3d = np.array(self.data3d, dtype=np.int64)
