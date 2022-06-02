#==========================#
# HPCSTRUCT1 PACKAGE FILE  #
#==========================#


from spack import *

class Hpcstruct1(Package):  # not a makefile package
    version('1.0', 'hpctest/tests/unit-tests/hpcstruct1')
    url = 'hpctest/tests/unit-tests/hpcstruct1'

    def install(self, spec, prefix):
        pass





