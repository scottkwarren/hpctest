#========================#
# MEMSTRESS PACKAGE FILE #
#========================#


from spack import *

class FibNoread(MakefilePackage):

    version('1.0', 'hpctest/tests/unit-tests/fib-noread')

    def install(self, spec, prefix):
    
        mkdirp(prefix.bin)
#       do not attempt:   install('fib-noread', prefix.bin)
#       == this test creates a fib-noread that can't be read  :-)





