import numpy as np

from peaq.peaqc import ffi, lib

'''
def pqeval(reference: np.ndarray, target: np.ndarray):
    xr = reference.flatten().astype(dtype=np.float64)
    xt = target.flatten().astype(dtype=np.float64)

    nsamp = xr.size

    PQ_NF = 2048
    PQ_CB_ADV = PQ_NF // 2

    opt = ffi.new('struct PQ_Opt *')
    lib.PQ_setopt(opt)

    Np = nsamp // PQ_CB_ADV - 1

    MOVC = lib.PQ_InitMOVC(1, Np)
    #MOVC.PD.c1 = opt.PDfactor
    MOVC.PD.c1 = 1.

    par = ffi.new('struct PQ_Par *')
    lib.PQgenTables(0, opt, par)

    fmem = ffi.new('struct PQ_FiltMem *')
    lib.PQinitFMem(par.CB.Nc, opt.PCinit, fmem)

    for i in range(Np):
        movbi = lib.PQeval(xr[i*PQ_CB_ADV:].ctypes.data, xt[i*PQ_CB_ADV:].ctypes.data, par, fmem)
        lib.PQframeMOVB(movbi, 1, i, MOVC)

    MOV = ffi.new('double[]', 11)  # PQ_NMOV_MAX
    lib.PQavgMOVB(MOVC, 1, 0, Np, MOV)

    di = ffi.new('double')
    ODG = lib.PQnNet(MOV, par.NNet, di)

    return list(MOV), di[0], ODG
'''

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