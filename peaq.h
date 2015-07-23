#include <libtsp.h>
#include <libtsp/AFpar.h>
#include <AO.h>

#include "afsp/audio/PQevalAudio/PQevalAudio.h"

void
PQ_InitMOVC (struct PQ_MOVBC *MOVC, int Nchan, int Np)

{
  int Ni, NC, N, j;
  double *x;
  double *xp;

  Ni = 2 * Np;
  NC = 11 * Np;
  if (Nchan == 1)
    N = Ni + NC;
  else
    N = Ni + 2 * NC;
  x = (double *) UTmalloc (N * sizeof (double));

  xp = x;
  MOVC->PD.Pc = xp;
  xp += Np;
  MOVC->PD.Qc = xp;
  xp += Np;

  for (j = 0; j < Nchan; ++j) {
    MOVC->Loud.NRef[j] = xp;
    xp += Np;
    MOVC->Loud.NTest[j] = xp;
    xp += Np;
    MOVC->MDiff.Mt1B[j] = xp;
    xp += Np;
    MOVC->MDiff.Mt2B[j] = xp;
    xp += Np;
    MOVC->MDiff.Wt[j] = xp;
    xp += Np;
    MOVC->NLoud.NL[j] = xp;
    xp += Np;
    MOVC->BW.BWRef[j] = xp;
    xp += Np;
    MOVC->BW.BWTest[j] = xp;
    xp += Np;
    MOVC->NMR.NMRavg[j] = xp;
    xp += Np;
    MOVC->NMR.NMRmax[j] = xp;
    xp += Np;
    MOVC->EHS.EHS[j] = xp;
    xp += Np;
  }

  assert (xp - x == N);
}

void peaqc_setopt(struct PQ_Opt *opt) {
    opt->Lp = 92.;
    opt->Ni = 0;
    opt->ClipMOV = 0;
    opt->PCinit = 0.;
    opt->PDfactor = 1.;
    opt->OverlapDelay = 1;
    opt->DataBounds = 0;
    opt->EndMin = PQ_NF / 2;
}

struct peaqc_result {
    double MOV[PQ_NMOV_MAX];
    double DI;
    double ODG;
};

struct peaqc_result peaqc_eval(const double *xr, const double *xt, size_t nsamp) {
//double peaqc_eval(const double *xr, const double *xt, size_t nsamp) {
    struct PQ_Opt opt;
    peaqc_setopt(&opt);

    size_t Np = nsamp / PQ_CB_ADV;

    struct PQ_MOVBC MOVC;
    PQ_InitMOVC(&MOVC, 1, Np);
    MOVC.PD.c1 = opt.PDfactor;

    struct PQ_Par par;
    PQgenTables(0, &opt, &par);

    struct PQ_FiltMem fmem;
    PQinitFMem(par.CB.Nc, opt.PCinit, &fmem);

    for (int i = 0; i < Np; i++) {
        struct PQ_MOVBI movbi = PQeval(xr+i*PQ_CB_ADV, xt+i*PQ_CB_ADV, &par, &fmem);
        PQframeMOVB(&movbi, 1, i, &MOVC);

        /*
        if (i % 50 == 0) {
            PQprtMOVCi (1, i, &MOVC);
        }
        */
    }

    struct peaqc_result results;

    PQavgMOVB(&MOVC, 1, 0, Np, results.MOV);

    double ODG = PQnNet(results.MOV, &(par.NNet), &(results.DI));
    results.ODG = ODG;

    return results;
}