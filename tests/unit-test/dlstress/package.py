#=======================#
# DLSTRESS PACKAGE FILE #
#=======================#


from spack import *

class Dlstress(MakefilePackage):

    version('1.0', 'hpctest/tests/unit-tests/dlstress')
    url = 'hpctest/tests/unit-tests/dlstress'

    def install(self, spec, prefix):
    
        mkdirp(prefix.bin)
        install('dlstress', prefix.bin)





