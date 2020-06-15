#=========================#
# FIB-NOREAD PACKAGE FILE #
#=========================#


from spack import *

class FibPg(MakefilePackage):

    version('1.0', 'hpctest/tests/unit-tests/fib-pg')

    def install(self, spec, prefix):
    
        mkdirp(prefix.bin)
        install('fib-bar',       prefix.bin)
        install('fib-pg-bar',    prefix.bin)
        install('fib-pg-bar-pg', prefix.bin)
        install('fib-bar-pg',    prefix.bin)





