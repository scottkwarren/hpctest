#==========================#
# CPP_THREADS PACKAGE FILE #
#==========================#


from spack import *

class CppThreads(MakefilePackage):

    version('1.0', 'hpctest/tests/unit-tests/cpp_threads')
    url = 'hpctest/tests/unit-tests/cpp_threads'

    def install(self, spec, prefix):
    
        mkdirp(prefix.bin)
        install('cpp_threads', prefix.bin)





