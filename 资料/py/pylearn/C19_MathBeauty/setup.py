from distutils.core import setup
from Cython.Build import cythonize

setup(name='Mandelbrot Computation',
      ext_modules=cythonize("MandelbrotComp.pyx"))
