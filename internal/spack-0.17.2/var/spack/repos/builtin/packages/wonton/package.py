# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Wonton(CMakePackage):
    """Wonton is a support package for the Portage
    (https://github.com/laristra/portage) and Tangram
    (https://github.com/laristra/tangram) libraries. It contains some
    mesh/state classes, wrappers for other mesh/state libraries and
    some utilities required by Portage and Tangram.

    """

    homepage = "https://portage.lanl.gov"
    git      = "https://github.com/laristra/wonton.git"
    url  = "https://github.com/laristra/wonton/releases/download/1.2.11/wonton-1.2.11.tar.gz"

    maintainers = ['raovgarimella']

    version('1.2.11', sha256='613436c799b392a99355db1cbf1062f1da39f3287eed665a5cd43bb65364d926')
    version('1.2.10', sha256='c5c2c99f040f1fa5a8da21ac5ccbbc5b226d1fd43ce3eb14c76d211601b65a72')
    version('1.2.1', sha256='4f00513d1abe86f256214d2b5171b1575b2cd464df8609307c24cbc4c595c305')

    variant('lapacke', default=True, description='Use LAPACKE solvers')

    # Variants for controlling parallelism
    variant('mpi', default=False, description='Enable distributed meshes with MPI')
    variant('thrust', default=False, description='Enable on-node parallelism using NVidia Thrust library')
    variant('kokkos', default=False, description='Enable on-node or device parallelism with Kokkos')
    variant('openmp', default=False, description="Enable on-node parallelism using OpenMP")
    variant('cuda', default=False, description="Enable GPU parallelism using CUDA")

    # wrappers to external mesh/state libraries
    variant('jali', default=False, description='Enable Jali mesh wrappers')

    conflicts('+jali ~mpi')    # Jali needs MPI
    conflicts('+thrust +cuda')  # Thrust with CUDA does not work as yet
    conflicts('+thrust +kokkos')  # Don't enable Kokkos, Thrust simultaneously

    # dependencies
    depends_on('cmake@3.13:', type='build')

    depends_on('netlib-lapack +lapacke', when='+lapacke')

    depends_on('mpi', when='+mpi')

    depends_on('jali +mstk', when='+jali')
    depends_on('mpi', when='+jali')

    # We need boost only when no thrust option
    depends_on('boost', when='~thrust')

    # NVidia thrust library
    depends_on('thrust@1.8.3', when='+thrust')

    # CUDA library
    depends_on('cuda', when='+cuda')

    # Kokkos with appropriate option
    depends_on('kokkos +openmp', when='+kokkos +openmp')
    depends_on('kokkos +cuda', when='+kokkos +cuda')

    def cmake_args(self):
        options = []
        if '+mpi' in self.spec:
            options.append('-DWONTON_ENABLE_MPI=ON')
        else:
            options.append('-DWONTON_ENABLE_MPI=OFF')

        if '+lapacke' in self.spec:
            options.append('-DWONTON_ENABLE_LAPACKE=ON')
            options.append('-DBLA_VENDOR=' + self.spec['blas'].name.upper())
            options.append(
                '-DBLAS_LIBRARIES=' + self.spec['blas'].libs.joined()
            )
        else:
            options.append('-DWONTON_ENABLE_LAPACKE=OFF')

        if '+thrust' in self.spec:
            options.append('-DWONTON_ENABLE_THRUST=ON')
            if '+cuda' in self.spec:
                options.append(
                    '-DTHRUST_HOST_BACKEND:STRING=THRUST_HOST_SYSTEM_CPP'
                )
                options.append(
                    '-DTHRUST_DEVICE_BACKEND:STRING=THRUST_DEVICE_SYSTEM_CUDA'
                )
            else:
                options.append(
                    '-DTHRUST_HOST_BACKEND:STRING=THRUST_HOST_SYSTEM_CPP'
                )
                options.append(
                    '-DTHRUST_DEVICE_BACKEND:STRING=THRUST_DEVICE_SYSTEM_OMP'
                )
        else:
            options.append('-DWONTON_ENABLE_THRUST=OFF')

        if '+kokkos' in self.spec:
            options.append('-DWONTON_ENABLE_Kokkos=ON')
            if '+cuda' in self.spec:
                options.append('-DWONTON_ENABLE_Kokkos_CUDA=ON')
            elif '+openmp' in self.spec:
                options.append('-DWONTON_ENABLE_Kokkos_OpenMP=ON')
        else:
            options.append('-DWONTON_ENABLE_Kokkos=OFF')

        if '+jali' in self.spec:
            options.append('-DWONTON_ENABLE_Jali=ON')
        else:
            options.append('-DWONTON_ENABLE_Jali=OFF')

        if '+flecsi' in self.spec:
            options.append('-DWONTON_ENABLE_FleCSI=ON')
        else:
            options.append('-DWONTON_ENABLE_FleCSI=OFF')

        # Unit test variant
        if self.run_tests:
            options.append('-DENABLE_UNIT_TESTS=ON')
            options.append('-DENABLE_APP_TESTS=ON')
        else:
            options.append('-DENABLE_UNIT_TESTS=OFF')
            options.append('-DENABLE_APP_TESTS=OFF')

        return options
