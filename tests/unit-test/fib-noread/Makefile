COMPILE=gcc -g 

TARGETS=fib-noread libfib.so


# create an unreadable executable to test hpctoolkit
# with circumstances we see at LLNL with 
# export-controlled apps
fib-noread: fib.c libfib.so
	$(COMPILE) -o fib-noread fib.c -Wl,-rpath=. libfib.so
	chmod -r $@

# note: if libfib.so is not readable, ld.so fails
#       therefore, we don't have to consider the case of
#       unreadable shared libraries 
libfib.so: libfib.c
	$(COMPILE) -shared -fPIC -o libfib.so libfib.c
	

fib-static:
	hpclink gcc -g -static -fopenmp -o fib-noread fib.c -lomp

clean:
	/bin/rm -rf $(TARGETS) hpctoolkit-* *.hpcstruct

dbclean:
	/bin/rm -rf hpctoolkit-*


run: fib-noread 
	hpcrun -e REALTIME ./fib-noread
	hpcprof hpctoolkit-fib-noread-measurements
#   hpcviewer hpctoolkit-fib-noread-database
