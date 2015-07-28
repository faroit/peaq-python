#include "libtsp.h"
#include "libtsp/AFpar.h"
#include "AO.h"

#include "PQevalAudio.h"

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

struct peaqc_vars {
    double FS;  /* Sampling frequency (double) */
    int NF;  /* Frame length */
    int CB_ADV;  /* Frame advance */
    int FB_ADV;  /* Sub-sampling factor in filter bank */
    double FCS;  /* Test sine frequency */
    double AMAX;  /* Max. input level corresponding to the max. listening level */
    int NL;  /* Number of correlation lags (EHS MOV) */
    int MAXNC;  /* Maximum number of channels */
    int NMOV_MAX;
};

void peaqc_getvars(struct peaqc_vars *vars) {
    vars->FS = PQ_FS;
    vars->NF = PQ_NF;
    vars->CB_ADV = PQ_CB_ADV;
    vars->FB_ADV = PQ_FB_ADV;
    vars->FCS = PQ_FCS;
    vars->AMAX = PQ_AMAX;
    vars->NL = PQ_NL;
    vars->MAXNC = PQ_MAXNC;
    vars->NMOV_MAX = PQ_NMOV_MAX;
}

void peaqc_defaultopt(struct PQ_Opt *opt) {
    opt->Lp = LP_DEFAULT;
    opt->Ni = 0;
    opt->ClipMOV = CLIP_MOV_DEFAULT;
    opt->PCinit = PC_INIT_DEFAULT;
    opt->PDfactor = PD_FACTOR_DEFAULT;
    opt->OverlapDelay = OVERLAP_DELAY_DEFAULT;
    opt->DataBounds = DATA_BOUNDS_DEFAULT;
    opt->EndMin = END_MIN_DEFAULT;
}

struct peaqc_result {
    double MOV[PQ_NMOV_MAX];
    double DI;
    double ODG;
};

void peaqc_eval(struct peaqc_result *results, const double *xr, const double *xt, size_t nsamp, struct PQ_Opt *opt) {
    size_t Np = nsamp / PQ_CB_ADV;

    struct PQ_MOVBC MOVC;
    PQ_InitMOVC(&MOVC, 1, Np);
    MOVC.PD.c1 = opt->PDfactor;

    struct PQ_Par par;
    PQgenTables(0, opt, &par);

    struct PQ_FiltMem fmem;
    PQinitFMem(par.CB.Nc, opt->PCinit, &fmem);

    for (int i = 0; i < Np; i++) {
        struct PQ_MOVBI movbi = PQeval(xr+i*PQ_CB_ADV, xt+i*PQ_CB_ADV, &par, &fmem);
        PQframeMOVB(&movbi, 1, i, &MOVC);

        if (opt->Ni != 0 && i % opt->Ni == 0) {
            PQprtMOVCi (1, i, &MOVC);
        }
    }

    PQavgMOVB(&MOVC, 1, 0, Np, results->MOV);

    double ODG = PQnNet(results->MOV, &(par.NNet), &(results->DI));
    results->ODG = ODG;
}