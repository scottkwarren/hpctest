# CC=/usr/bin/gcc

all: fib fib.hpcstruct

fib:
	hpclink -v $(CC) -g -static -o fib fib.c
	
fib.hpcstruct: fib
	hpcstruct fib

run: all
	HPCRUN_EVENT_LIST=REALTIME fib
	hpcprof -S fib.hpcstruct hpctoolkit-fib-measurements
#	hpcviewer hpctoolkit-fib-database
