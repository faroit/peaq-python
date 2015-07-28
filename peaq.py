import numpy as np

from peaq.peaqc import ffi, lib

def pqvars():
    vars = ffi.new('struct peaqc_vars *')
    lib.peaqc_getvars(vars)
    return vars

def pqopt():
    opt = ffi.new('struct PQ_Opt *')
    lib.peaqc_defaultopt(opt)
    return opt

def pqeval(reference: np.ndarray, target: np.ndarray, scale, options=None):
    if options is None:
        options = pqopt()

    xr = reference.flatten().astype(dtype=np.float64)
    xr *= scale
    xt = target.flatten().astype(dtype=np.float64)
    xt *= scale

    pr = ffi.cast('double const *', xr.ctypes.data)
    pt = ffi.cast('double const *', xt.ctypes.data)

    results = ffi.new('struct peaqc_result *')
    lib.peaqc_eval(results, pr, pt, min(xr.size, xt.size), options)
    return results.ODG