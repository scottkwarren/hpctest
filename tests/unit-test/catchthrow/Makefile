#
#  Makefile for catch-throw stress test.
#

CFLAGS = -g

PROGS = catchthrow

TIMELIMIT = 120

all: ${PROGS}

catchthrow: catchthrow.cc
	$(CXX) $(CFLAGS) -o $@ catchthrow.cc

test: ${PROGS}
	export HPCRUN_ABORT_TIMEOUT=$(TIMELIMIT); hpcrun -t -e REALTIME@250 catchthrow

clobber:
	/bin/rm -rf hpctoolkit* hpcstruct* core.*

clean: clobber
	rm -f $(PROGS)

