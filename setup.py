from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        'parqueadero_cpp',
        ['cpp/parqueadero.cpp', 'cpp/bindings.cpp'],
        include_dirs=[pybind11.get_include(), 'cpp'],
        language='c++',
        extra_compile_args=['-std=c++11'],
    ),
]

setup(
    name='parqueadero_cpp',
    version='1.0',
    ext_modules=ext_modules,
    install_requires=['pybind11'],
)