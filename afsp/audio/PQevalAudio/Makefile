#
#	Makefile for PQevalAudio
#

PROG = PQevalAudio
OBJECTS = \
	PQevalAudio.o \
	PQeval.o \
	PQnNet.o \
	CB/PQgroupCB.o \
	CB/PQspreadCB.o \
	CB/PQtimeSpread.o \
	Misc/PQdataBoundary.o \
	Misc/PQgenTables.o \
	Misc/PQinitFmem.o \
	Misc/PQoptions.o \
	Misc/PQreadChan.o \
	Misc/PQtableFn.o \
	MOV/PQframeMOV.o \
	MOV/PQloudTest.o \
	MOV/PQmovBW.o \
	MOV/PQmovEHS.o \
	MOV/PQmovModDiffB.o \
	MOV/PQmovNLoudB.o \
	MOV/PQmovNMRB.o \
	MOV/PQmovPD.o \
	MOV/PQprtMOV.o \
	MOV/PQprtMOVCi.o \
	Patt/PQadapt.o \
	Patt/PQmodPatt.o \
	Patt/PQloud.o \
	#

HEADERS = PQevalAudio.h

SHELL = /bin/sh

dist_dir = ../..

dist_libdir = $(dist_dir)/lib
dist_bindir = $(dist_dir)/bin
dist_includedir = $(dist_dir)/include

EXEEXT =
COPTS = -O -fPIC
CFLAGS = $(COPTS) -I$(dist_includedir) -I. -ICB
LDFLAGS = -s -lm

LLIBS = $(dist_libdir)/libAO.a $(dist_libdir)/libtsplite.a

.PHONY: mostlyclean clean

LIB=$(dist_libdir)/lib$(PROG).a

$(LIB): $(OBJECTS)
	$(AR) rcs $@ $+
	ranlib $@

$(OBJECTS): $(HEADERS)

mostlyclean:
	rm -f *.o
clean:	mostlyclean
	rm -f $(BIN) $(LIB)
