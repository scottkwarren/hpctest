#======================#
# NEKBONE PACKAGE FILE #
#======================#


from spack import *

class Nekbone(MakefilePackage):
    """Nekbone is captures the basic structure and user interface of the
        extensive Nek5000 software. Nek5000 is a high order, incompressible
        Navier-Stokes solver based on the spectral element method. It has
        a wide range of applications and intricate customizations available
        to users. Nekbone, on the other hand, solves a Helmholtz equation
        in a box, using the spectral element method. It is pared down to
        include only the necessary features to compile, run, and solve the
        applications found in the test/ directory. Since almost all practical
        applications are in the three dimensional space, the solver is
        set to work with three dimensional geometries as default. Nekbone
        solves a standard Poisson equation using a conjugate gradient iteration
        with a simple preconditioner on a block or linear geometry (set
        within the test directory of the simulation). Nekbone exposes the
        principal computational kernel to reveal the essential elements of
        the algorithmic-architectural coupling that is pertinent to Nek5000. 
    """

    homepage = "https://cesar.mcs.anl.gov/content/software/thermal hydraulics"
    url      = "https://github.com/HPCToolkit/HPCTest"

    version('1.0', 'app/nekbone-2.3.4')
    variant('openmp', description='Build with OpenMP support', default=True)
    variant('mpi', description='Build with MPI support', default=True)
    depends_on('mpi', when='+mpi')

    @property
    def build_targets(self):
        
        targets = []
        languages = 'CC = {} F90 = {}'.format(spack_cc, spack_fc)
        cflags = '-g -O3'
        fflags = '-g -O3'
        lflags = '-g -O3'
        
        if '+openmp' in self.spec:
            cflags += ' ' + self.compiler.openmp_flag
            lflags += ' ' + self.compiler.openmp_flag
        
        if '+mpi' in self.spec:
            languages = 'CC={} F77={}'.format(self.spec['mpi'].mpicc, self.spec['mpi'].mpifc) # sic 'F77' b/c makefile uses it for f90 (!)
            targets.append('USE_MPI=1')

        targets.append(languages)
        targets.append('CFLAGS="{0}"'.format(cflags))
        targets.append('FFLAGS="{0}"'.format(fflags))
        targets.append('LFLAGS="{0}"'.format(lflags))
        
        return targets

    def build(self, spec, prefix):
        """Runs specified command, passing :py:attr:`~.MakefilePackage.build_targets`
        as targets.
        """
####    import os
        from os.path import join
        from subprocess import call
        call("env {} ./makenek ex1".format(" ".join(self.build_targets)),
             shell=True, cwd=join(self.build_directory, "test", "example1"))

    def install(self, spec, prefix):
        
        mkdirp(prefix.bin)
        install('test/example1/nekbone', prefix.bin)
        install('test/example1/data.rea', prefix.bin)
        install('test/example1/SIZE', prefix.bin)





