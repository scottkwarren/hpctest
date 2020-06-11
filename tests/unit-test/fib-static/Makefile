# CC=/usr/bin/gcc

fib:
	hpclink -v $(CC) -g -static -o fib fib.c
	
fib.hpcstruct:
	hpcstruct fib

run: fib fib.hpcstruct
	HPCRUN_EVENT_LIST=REALTIME ./fib
	hpcprof -S fib.hpcstruct hpctoolkit-fib-measurements
#	hpcviewer hpctoolkit-fib-database
