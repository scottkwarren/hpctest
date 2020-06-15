#============================#
# FIB-PG-STATIC PACKAGE FILE #
#============================#


from spack import *

class FibPgStatic(MakefilePackage):

    version('1.0', 'hpctest/tests/unit-tests/fib-pg-static')

    def install(self, spec, prefix):
    
        mkdirp(prefix.bin)
        install('fib-static',    prefix.bin)
        install('fib-pg-static', prefix.bin)





