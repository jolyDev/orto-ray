import os

PATH_TO_EXE = r"E:\DicomCompressor\DICOM_Compressor\bin360nt\bin\dcmcjpeg.exe"
INPUT = r"E:\orto-ray\Data\Airway"
OUTPUT = r"E:\DicomCompressor\Result"
CMD = r"{} -v +eb +q 70 {} {}\{}"

files = []
for (r, d, f) in os.walk(INPUT):
    for file in f:
        if '.dcm' in file:
            command = CMD.format(PATH_TO_EXE, os.path.join(INPUT, file), OUTPUT, file)
            print(command)
            os.system(command)


print("Done")
print(OUTPUT)