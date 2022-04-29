# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class Blaspp(CMakePackage, CudaPackage, ROCmPackage):
    """C++ API for the Basic Linear Algebra Subroutines. Developed by the
       Innovative Computing Laboratory at the University of Tennessee,
       Knoxville."""

    homepage = 'https://bitbucket.org/icl/blaspp'
    git = homepage
    url = 'https://bitbucket.org/icl/blaspp/downloads/blaspp-2020.09.00.tar.gz'
    maintainers = ['teonnik', 'Sely85', 'G-Ragghianti', 'mgates3']

    version('master', branch='master')
    version('2021.04.01', sha256='11fc7b7e725086532ada58c0de53f30e480c2a06f1497b8081ea6d8f97e26150')
    version('2020.10.02', sha256='36e45bb5a8793ba5d7bc7c34fc263f91f92b0946634682937041221a6bf1a150')
    version('2020.10.01', sha256='1a05dbc46caf797d59a7c189216b876fdb1b2ff3e2eb48f1e6ca4b2756c59153')
    version('2020.10.00', sha256='ce148cfe397428d507c72d7d9eba5e9d3f55ad4cd842e6e873c670183dcb7795')

    variant('openmp', default=True, description='Use OpenMP internally.')
    variant('shared', default=True, description='Build shared libraries')

    depends_on('cmake@3.15.0:', type='build')
    depends_on('blas')
    depends_on('llvm-openmp', when='%apple-clang +openmp')
    depends_on('rocblas', when='+rocm')

    # only supported with clingo solver: virtual dependency preferences
    # depends_on('openblas threads=openmp', when='+openmp ^openblas')

    # BLAS++ tests will fail when using openblas > 0.3.5 without multithreading support
    # locking is only supported in openblas 3.7+
    conflicts('^openblas@0.3.6 threads=none', msg='BLAS++ requires a threadsafe openblas')
    conflicts('^openblas@0.3.7: ~locking', msg='BLAS++ requires a threadsafe openblas')

    conflicts('+rocm', when='@:2020.10.02', msg='ROCm support requires BLAS++ 2021.04.00 or greater')
    conflicts('+rocm', when='+cuda', msg='BLAS++ can only support one GPU backend at a time')

    def cmake_args(self):
        spec = self.spec
        backend_config = '-Duse_cuda=%s' % ('+cuda' in spec)
        if self.version >= Version('2021.04.01'):
            backend = 'none'
            if '+cuda' in spec:
                backend = 'cuda'
            if '+rocm' in spec:
                backend = 'hip'
            backend_config = '-Dgpu_backend=%s' % backend
        return [
            '-Dbuild_tests=%s'       % self.run_tests,
            '-Duse_openmp=%s'        % ('+openmp' in spec),
            '-DBUILD_SHARED_LIBS=%s' % ('+shared' in spec),
            backend_config,
            '-DBLAS_LIBRARIES=%s'    % spec['blas'].libs.joined(';')
        ]

    def check(self):
        # If the tester fails to build, ensure that the check() fails.
        if os.path.isfile(join_path(self.build_directory, 'test', 'tester')):
            with working_dir(self.build_directory):
                make('check')
        else:
            raise Exception('The tester was not built!')
