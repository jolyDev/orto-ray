import setuptools  # important
from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
    ext_modules = cythonize(["regionGrowth2D.pyx", "regionGrowth3D.pyx"],
                            compiler_directives={'language_level': "3"}),
    include_dirs = [numpy.get_include()]
)