def readstring(fn):
    with open(fn, mode='rt') as f:
        return f.read()

from cffi import FFI
ffi = FFI()

ffi.set_source(
    'peaqc',
    readstring('peaq/peaq.h'),
    library_dirs=[
        'peaq/afsp/lib',
    ],
    libraries=[
        'PQevalAudio',
        'AO',
        'tsplite',
    ],
    include_dirs=[
        'peaq/afsp/include',
        'peaq/afsp/audio/PQevalAudio'
    ],
    extra_objects=[],
    extra_compile_args=['-std=c99']
)

ffi.cdef(readstring('peaq/peaq.cdef'))

if __name__ == '__main__':
    ffi.compile()