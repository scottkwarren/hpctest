# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Arrayfire(CMakePackage, CudaPackage):
    """ArrayFire is a high performance software library for parallel computing
    with an easy-to-use API. Its array based function set makes parallel
    programming more accessible."""

    homepage = "https://arrayfire.org/docs/index.htm"
    git      = "https://github.com/arrayfire/arrayfire.git"

    version('master', submodules=True)
    version('3.7.3', submodules=True, tag='v3.7.3')
    version('3.7.2', submodules=True, tag='v3.7.2')
    version('3.7.0', submodules=True, tag='v3.7.0')

    variant('cuda',   default=False, description='Enable Cuda backend')
    variant('forge',   default=False, description='Enable graphics library')
    variant('opencl', default=False, description='Enable OpenCL backend')

    depends_on('boost@1.65:')
    depends_on('fftw-api@3:')
    depends_on('blas')
    depends_on('cuda@7.5:', when='+cuda')
    depends_on('cudnn', when='+cuda')
    depends_on('opencl +icd', when='+opencl')
    # TODO add more opencl backends:
    # currently only Cuda backend is enabled
    # https://github.com/arrayfire/arrayfire/wiki/Build-Instructions-for-Linux#opencl-backend-dependencies

    depends_on('fontconfig', when='+forge')
    depends_on('glfw@3.1.4:', when='+forge')

    @property
    def libs(self):
        query_parameters = self.spec.last_query.extra_parameters

        libraries = []
        if 'cpu' in query_parameters:
            libraries.append('libafcpu')
        if 'cuda' in query_parameters and '+cuda' in self.spec:
            libraries.append('libafcuda')
        if 'opencl' in query_parameters and '+opencl' in self.spec:
            libraries.append('libafopencl')
        if not query_parameters or 'unified' in query_parameters:
            libraries.append('libaf')

        return find_libraries(libraries, root=self.prefix, recursive=True)

    def cmake_args(self):
        args = []
        args.extend([
            self.define_from_variant('AF_BUILD_CUDA', 'cuda'),
            self.define_from_variant('AF_BUILD_FORGE', 'forge'),
            self.define_from_variant('AF_BUILD_OPENCL', 'opencl'),
        ])
        if '^mkl' in self.spec:
            args.append('-DUSE_CPU_MKL=ON')
            if '%intel' not in self.spec:
                args.append('-DMKL_THREAD_LAYER=GNU OpenMP')

        return args
