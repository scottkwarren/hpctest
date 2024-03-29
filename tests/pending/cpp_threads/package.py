#==========================#
# CPP_THREADS PACKAGE FILE #
#==========================#


from spack import *

class CppThreads(MakefilePackage):

    version('1.0', 'unit-tests/cpp_threads')

    @property
    def build_targets(self):
        
        targets = []
        targets.append('-f')
        targets.append("Makefile.hpctest")
        targets.append('CXXFLAGS = -std=gnu++11')
        return targets

    def install(self, spec, prefix):
        
        mkdirp(prefix.bin)
        install('fib', prefix.bin)





