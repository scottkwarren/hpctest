#========================#
# MEMSTRESS PACKAGE FILE #
#========================#


from spack import *

class Memstress(MakefilePackage):

    version('1.0', 'hpctest/tests/unit-tests/memlstress')

    def install(self, spec, prefix):
    
        mkdirp(prefix.bin)
        install('memstress', prefix.bin)





