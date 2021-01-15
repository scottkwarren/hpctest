#========================#
# MEMSTRESS PACKAGE FILE #
#========================#


from spack import *

class Memstress(MakefilePackage):

    version('1.0', 'hpctest/tests/unit-tests/memstress')
    url = 'hpctest/tests/unit-tests/memstress'

    def install(self, spec, prefix):
    
        mkdirp(prefix.bin)
        install('memstress', prefix.bin)





