# CC=/usr/bin/$(CC)

all: fib-bar fib-pg-bar fib-pg-bar-pg fib-bar-pg 


fib-bar: fib.c bar.so
	$(CC) -o $@  fib.c -Wl,-rpath=`pwd` bar.so 

fib-pg-bar: fib.c bar-pg.so
	$(CC) -o $@  -pg fib.c -Wl,-rpath=`pwd` bar.so 

fib-pg-bar-pg: fib.c bar-pg.so
	$(CC) -o $@  -pg fib.c -Wl,-rpath=`pwd` bar-pg.so 

fib-bar-pg: fib.c bar-pg.so
	$(CC) -o $@  fib.c -Wl,-rpath=`pwd` bar-pg.so 


bar.so: bar.c
	$(CC) -shared -fPIC -o bar.so bar.c

bar-pg.so: bar.c
	$(CC) -shared -fPIC -pg -o bar-pg.so bar.c



