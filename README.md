# peaq-python

:warning: This is based on a [bitbucket repo](https://bitbucket.org/dinhngtu/peaq-python) and currently not working

Requirements for building Python bindings for AFsp PQevalAudio:
* Python + NumPy + CFFI
* C compiler
* AFsp source code (http://www-mmsp.ece.mcgill.ca/documents/Software/)
  Put AFsp source code in afsp/

Tested on Python 3.4 with NumPy 1.8.2 and CFFI 1.1.2, using AFsp v9r0.

How to build:
Simply run 'python setup.py install'.
Read the source for how to use the API.
Testing is done by comparing output with that of the PQevalAudio executable.
No unit test available yet.

Warning:
This library includes source code from the AFsp software package.
Use this library at your own risk.
The author asserts no copyright over this library.
