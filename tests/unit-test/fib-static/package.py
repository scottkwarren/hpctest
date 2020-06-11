#=========================#
# FIB-NOREAD PACKAGE FILE #
#=========================#


from spack import *

class FibStatic(MakefilePackage):

    version('1.0', 'hpctest/tests/unit-tests/fib-static')

    def install(self, spec, prefix):
    
        mkdirp(prefix.bin)
        install('fib', prefix.bin)





