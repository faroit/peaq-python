def readstring(fn):
    with open(fn, mode='rt') as f:
        return f.read()

import os

os.chdir('afsp')
os.system('make clean')
os.system("make 'COPTS=-O -fPIC'")
os.chdir('audio/PQevalAudio')
os.system('make -f ../../../Makefile.PQevalAudio')
os.chdir('../../..')

from cffi import FFI
ffi = FFI()

ffi.set_source(
    'peaqc',
    readstring('peaq/peaq.h'),
    library_dirs=[
        'afsp/lib',
    ],
    libraries=[
        'PQevalAudio',
        'AO',
        'tsplite',
    ],
    include_dirs=[
        'afsp/include',
        'afsp/audio/PQevalAudio'
    ],
    extra_objects=[],
    extra_compile_args=['-std=c99']
)

ffi.cdef(readstring('peaq/peaq.cdef'))

if __name__ == '__main__':
    ffi.compile()