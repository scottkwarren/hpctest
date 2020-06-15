# CC=/usr/bin/gcc

all: fib-static fib-pg-static 

fib-static: fib.c 
	hpclink gcc -o $@  -static fib.c 

fib-pg-static: fib.c 
	hpclink gcc -o $@  -pg -static fib.c 


