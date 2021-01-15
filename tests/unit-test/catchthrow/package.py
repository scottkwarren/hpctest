#=========================#
# CATCHTHROW PACKAGE FILE #
#=========================#


from spack import *

class Catchthrow(MakefilePackage):

    version('1.0', 'hpctest/tests/unit-tests/catchthrow')
    url = 'hpctest/tests/unit-tests/catchthrow'

    def install(self, spec, prefix):
    
        mkdirp(prefix.bin)
        install('catchthrow', prefix.bin)





