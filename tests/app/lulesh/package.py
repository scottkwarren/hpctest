#=====================#
# LULESH PACKAGE FILE #
#=====================#


from spack import *

class Lulesh(MakefilePackage):
    """Many important simulation problems of interest to DOE involve complex multi-material
    systems that undergo large deformations. LULESH is a highly simplified application
    that represents the numerical algorithms, data motion, and programming style typical
    in scientific C or C++ based hydrodynamic applications. The Shock Hydrodynamics
    Challenge Problem was originally defined and implemented by LLNL as one of five
    challenge problems in the DARPA UHPC program and has since become a widely studied
    proxy application in DOE co-design efforts for exascale. It has been ported to a number
    of programming models and optimized for a number of advanced platforms. 
    """

    homepage = "https://codesign.llnl.gov/lulesh.php"
    url      = "https://github.com/HPCToolkit/HPCTest"

    version('1.0', 'app/lulesh')
    variant('openmp', description='Build with OpenMP support', default=True)
    variant('mpi', description='Build with MPI support', default=True)
    depends_on('mpi', when='+mpi')

    @property
    def build_targets(self):
        
        targets = []
        languages = 'CXX = {}'.format(spack_cxx)
        cxxflags = '-g -O3'
        ldflags = '-g -O3'

        if '+openmp' in self.spec:
            cxxflags += ' ' + self.compiler.openmp_flag
            ldflags  += ' ' + self.compiler.openmp_flag
        
        if '+mpi' in self.spec:
            languages = 'CXX = {}'.format(self.spec['mpi'].mpicxx)
            cxxflags += ' ' + '-DUSE_MPI=1'
            targets.append('MPI_INC = {0}'.format(self.spec['mpi'].prefix.include))
            targets.append('MPI_LIB = {0}'.format(self.spec['mpi'].prefix.lib))

        targets.append(languages)
        targets.append('CXXFLAGS = {0}'.format(cxxflags))
        targets.append('LDFLAGS = {0}'.format(ldflags))
        
        return targets

    def install(self, spec, prefix):
        
        mkdirp(prefix.bin)
        install('lulesh2.0', prefix.bin)





