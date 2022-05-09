#==========================#
# HPCSTRUCT1 PACKAGE FILE  #
#==========================#


from spack import *

class HPCstruct1(MakefilePackage):

    version('1.0', 'hpctest/tests/unit-tests/hpcstruct1')
    url = 'hpctest/tests/unit-tests/hpcstruct1'

    def install(self, spec, prefix):
    
	pass





