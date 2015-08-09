from setuptools import setup, find_packages

setup(
    name='afsp-peaq-python',
    version='1.0',
    packages=['peaq'],
    ext_package='peaq',
    setup_requires=['cffi>=1.0.0'],
    install_requires=['numpy>=1.8', 'cffi>=1.0.0'],
    cffi_modules=['_cffi_build/peaq_build.py:ffi']
)