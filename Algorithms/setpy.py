import setuptools  # important
from distutils.core import setup
from Cython.Build import cythonize
import numpy

#cmd to compile
"python setpy.py build_ext —-inplace"

#cmd to generate report
"cython -a Trim.pyx"

setup(
    ext_modules = cythonize(["regionGrowth2D.pyx", "regionGrowth3D.pyx", "Trim.pyx"],
                            compiler_directives={'language_level': "3"}),
    include_dirs = [numpy.get_include()]
)