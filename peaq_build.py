def readstring(fn):
    with open(fn, mode='rt') as f:
        return f.read()

from cffi import FFI
ffi = FFI()

ffi.set_source(
    'peaqc',
    readstring('peaq.h'),
    library_dirs=[
        'afsp/lib',
    ],
    libraries=[
        'PQevalAudio',
        'AO',
        'tsplite',
    ],
    include_dirs=['afsp/include'],
    extra_objects=[],
    extra_compile_args=['-std=c99']
)

ffi.cdef(readstring('peaq.cdef'))

if __name__ == '__main__':
    ffi.compile()