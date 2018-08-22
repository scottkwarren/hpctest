#=================================================#
# AMG2013 PACKAGE FILE TO BE GENERATED BY HPCTEST #
#=================================================#


# from info.name, info.description, and build.kind
from spack import *
class CppThreads(MakefilePackage):
    """ This microkernel contains three compute-intensive sections of the larger AMG benchmark.
        Optimizing performance for these three sections will improve the figure of merit of AMG.
        AMGmk, like the full AMG benchmark, is written in C. The three sections chosen to create
        this benchmark perform compressed sparse row (CSR) matrix vector multiply, algebraic
        multigrid (AMG) mesh relaxation, and a simple a * X + Y vector operation. OpenMP
        directives allow additional increases in performance. AMGmk uses no MPI parallelism and
        is meant to be studied as a single-CPU benchmark or OpenMP benchmark only. The run time
        of this benchmark is not linearly related to the figure of merit of the larger AMG
        benchmark because the exact proportion of time spent performing these three operations
        varies depending on the size of the problem and the specific linear system being solved. 
    """

# from info.homepage and info.url
    homepage = ""
    url      = "https://github.com/HPCToolkit/HPCTest"

# from info.version
    version('1.0', 'unit-tests/cpp_threads')

# from config.'default variants' swfault value
    variant('plain', description='Uses pthreads controlled manually.', default=True)

# boilerplate for config.variants[@plain].flags...
    @property
    def build_targets(self):
        targets = []
        
## from config.variants[@plain].languages
##    languages: [ cxx ]
        languages = 'CXX = {}'.format(spack_cxx)
        
## from config.variants[@plain].flags
        cxxflags = "-std=gnu++11"
        
## from config.makefilename
        targets.append('-f')
        targets.append("Makefile.hpctest")
        
# boilerplate closing 'build_targets'
        targets.append(languages)
        targets.append('CXXFLAGS = {0}'.format(cxxflags))
        return targets

# from build.install
    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('fib', prefix.bin)




