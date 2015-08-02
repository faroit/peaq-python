import numpy as np

from peaq.peaqc import ffi, lib


def pqvars():
    vars = ffi.new('struct peaqc_vars *')
    lib.peaqc_getvars(vars)
    return vars

_vars = pqvars()


def pqopt():
    opt = ffi.new('struct PQ_Opt *')
    lib.peaqc_defaultopt(opt)
    return opt


def pqeval(reference: np.ndarray, target: np.ndarray, options=None):
    """
    :param reference: reference sound input, must be 48 kHz float
    :param target: sound input to compare, must be 48 kHz float
    :param options: appropriate PQ_Opt object or None
    :return: tuple (distortion index, objective difference grade)
    """

    if options is None:
        options = pqopt()

    NF, ADV = _vars.NF, _vars.CB_ADV
    Q = NF // ADV

    nsamp = min(reference.size, target.size)
    nblocks = (nsamp + ADV - 1) // ADV
    # pad enough for last block
    bufcount = (nblocks + Q - 1) * ADV

    xr = np.empty(bufcount, dtype=np.float64)
    xr[:nsamp] = reference.ravel()[:nsamp] * 32768.
    xr[nsamp:] = 0
    xt = np.empty(bufcount, dtype=np.float64)
    xt[:nsamp] = target.ravel()[:nsamp] * 32768.
    xt[nsamp:] = 0

    pr = ffi.cast('double const *', xr.ctypes.data)
    pt = ffi.cast('double const *', xt.ctypes.data)

    results = ffi.new('struct peaqc_result *')
    lib.peaqc_eval(results, pr, pt, nsamp, options)
    return results.DI, results.ODG


class pqref:
    def __init__(self, reference, options=None):
        if options is None:
            self.options = pqopt()
        else:
            self.options = options

        self.reference = reference * 32768.

    def evaluate(self, target):
        target_scaled = target * 32768.

        nsamp = min(self.reference.size, target_scaled.size)

        pr = ffi.cast('double const *', self.reference.ctypes.data)
        pt = ffi.cast('double const *', target_scaled.ctypes.data)

        results = ffi.new('struct peaqc_result *')
        lib.peaqc_eval_safe(results, pr, pt, nsamp, self.options)
        return results.DI, results.ODG
