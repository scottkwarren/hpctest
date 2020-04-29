#======================#
# AMG2013 PACKAGE FILE #
#======================#


from spack import *

class Amg2013(MakefilePackage):
    """AMG2013 is a parallel algebraic multigrid solver for linear systems arising from
       problems on unstructured grids.  The driver provided with AMG2013 builds linear 
       systems for various 3-dimensional problems.
       AMG2013 is written in ISO-C.  It is an SPMD code which uses MPI and OpenMP 
       threading within MPI tasks. Parallelism is achieved by data decomposition. The 
       driver provided with AMG2013 achieves this decomposition by simply subdividing 
       the grid into logical P x Q x R (in 3D) chunks of equal size. 
    """

    homepage = "https://codesign.llnl.gov/amg2013.php"
    url      = "https://github.com/HPCToolkit/HPCTest-tests"

    version('1.0', 'app/AMG2013')
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
        install('test/amg2013', prefix.bin)
        install('test/sstruct.in.MG.FD', prefix.bin)





