# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Damaris(CMakePackage):
    """Damaris is a middleware for asynchronous I/O and in situ analytics
    targeting large-scale, MPI-based HPC simulations."""

    homepage = "https://project.inria.fr/damaris/"
    git      = "https://gitlab.inria.fr/Damaris/damaris.git"
    maintainers = ['jcbowden']

    version('1.5.0',  tag='v1.5.0')
    version('1.3.3',  tag='v1.3.3')
    version('1.3.2',  tag='v1.3.2')
    version('1.3.1',  tag='v1.3.1')

    variant('fortran',  default=True,  description='Enables Fortran support')
    variant('hdf5',     default=False, description='Enables the HDF5 storage plugin')
    variant('static',   default=False, description='Builds a static version of the library')
    variant('catalyst', default=False, description='Enables the Catalyst visualization plugin')
    variant('visit',    default=False, description='Enables the VisIt visualization plugin')
    variant('examples', default=False, description='Enables compilation and installation of the examples code')

    depends_on('mpi')
    depends_on('cmake@3.18.0:', type=('build'))
    depends_on('boost +thread+log+filesystem+date_time @1.67:')
    depends_on('xsd')
    depends_on('xerces-c')
    depends_on('hdf5@1.8.20:', when='+hdf5')
    depends_on('paraview+python3', when='+catalyst')
    depends_on('visit+mpi', when='+visit')

    def cmake_args(self):
        args = []
        if(not self.spec.variants['static'].value):
            args.extend(['-DBUILD_SHARED_LIBS=ON'])
        args.extend(['-DCMAKE_CXX_COMPILER=%s' % self.spec['mpi'].mpicxx])
        args.extend(['-DCMAKE_C_COMPILER=%s' % self.spec['mpi'].mpicc])
        args.extend(['-DBOOST_ROOT=%s' % self.spec['boost'].prefix])
        args.extend(['-DXercesC_ROOT=%s' % self.spec['xerces-c'].prefix])
        args.extend(['-DXSD_ROOT=%s' % self.spec['xsd'].prefix])

        if (self.spec.variants['fortran'].value):
            args.extend(['-DCMAKE_Fortran_COMPILER=%s'
                         % self.spec['mpi'].mpifc])
            args.extend(['-DENABLE_FORTRAN:BOOL=ON'])

        if (self.spec.variants['hdf5'].value):
            args.extend(['-DENABLE_HDF5:BOOL=ON'])
            args.extend(['-DHDF5_ROOT:PATH=%s' % self.spec['hdf5'].prefix])

        if (self.spec.variants['catalyst'].value):
            args.extend(['-DENABLE_CATALYST:BOOL=ON'])
            args.extend(['-DParaView_ROOT:PATH=%s'
                         % self.spec['catalyst'].prefix])

        if (self.spec.variants['examples'].value):
            args.extend(['-DENABLE_EXAMPLES:BOOL=ON'])

        if (self.spec.variants['visit'].value):
            args.extend(['-DENABLE_VISIT:BOOL=ON'])
            args.extend(['-DVisIt_ROOT:PATH=%s' % self.spec['visit'].prefix])
        return args
