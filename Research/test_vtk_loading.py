import SimpleITK
import pyvista as pv

def test(data):
    dataX = pv.wrap(data)
    dataX.plot(volume=True, eye_dome_lighting=True, parallel_projection=True) # Volume render


dicom_location = "E:/orto-ray/dicom_data/head"
reader = SimpleITK.ImageSeriesReader()
reader.SetFileNames(reader.GetGDCMSeriesFileNames(dicom_location))
data = SimpleITK.GetArrayFromImage(reader.Execute())

test(data)