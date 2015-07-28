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
    readstring('_cffi_build/peaq.h'),
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

ffi.cdef(readstring('_cffi_build/peaq.cdef'))

if __name__ == '__main__':
    ffi.compile()