#=======================#
# AMG2013 PACKAGE FILE  #
#=======================#


from spack import *

class Amg2006(MakefilePackage):
    """AMG2006 is a parallel algebraic multigrid solver for linear systems arising
    from problems on unstructured grids. 
    """

    homepage = "https://svn.mcs.anl.gov/repos/performance/benchmarks/AMG2006"
    url      = "https://github.com/HPCToolkit/HPCTest"

    version('1.0', 'app/AMG2006')
    variant('openmp', description='Build with OpenMP support', default=True)
    variant('mpi', description='Build with MPI support', default=True)
    depends_on('mpi', when='+mpi')

    @property
    def build_targets(self):
        
        targets = []
        languages = 'CC = {}'.format(spack_cc)
        cxxflags = '-g -O2'
        ldflags = '-lm'
        
        if '+openmp' in self.spec:
            cxxflags += ' ' + '-DHYPRE_USING_OPENMP'
            cxxflags += ' ' + self.compiler.openmp_flag
            ldflags  += ' ' + self.compiler.openmp_flag
        
        if '+mpi' in self.spec:
            languages = 'CC = {}'.format(self.spec['mpi'].mpicc)
            cxxflags += ' ' + '-DUSE_MPI=1'
            targets.append('MPI_INC = {0}'.format(self.spec['mpi'].prefix.include))
            targets.append('MPI_LIB = {0}'.format(self.spec['mpi'].prefix.lib))

        targets.append(languages)
        targets.append('INCLUDE_CFLAGS = {0}'.format(cxxflags))
        targets.append('INCLUDE_LFLAGS = {0}'.format(ldflags))
        
        return targets

    def install(self, spec, prefix):
        
        mkdirp(prefix.bin)
        install('test/amg2006', prefix.bin)
        install('test/sstruct.in.AMG.FD', prefix.bin)





