# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libbeagle(AutotoolsPackage, CudaPackage):
    """Beagle performs genotype calling, genotype phasing, imputation of
       ungenotyped markers, and identity-by-descent segment detection."""

    homepage = "https://github.com/beagle-dev/beagle-lib"
    url      = "https://github.com/beagle-dev/beagle-lib/archive/v3.1.2.tar.gz"

    version('3.1.2', sha256='dd872b484a3a9f0bce369465e60ccf4e4c0cd7bd5ce41499415366019f236275')
    version('2.1.2', sha256='82ff13f4e7d7bffab6352e4551dfa13afabf82bff54ea5761d1fc1e78341d7de',
            url='https://github.com/beagle-dev/beagle-lib/archive/beagle_release_2_1_2.tar.gz')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    depends_on('subversion', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('java', type='build')

    cuda_arch_values = CudaPackage.cuda_arch_values
    variant(
        'cuda_arch',
        description='CUDA architecture',
        default='none',
        values=('none',) + cuda_arch_values,
        multi=False
    )
    conflicts('cuda_arch=none', when='+cuda',
              msg='must select a CUDA architecture')

    def patch(self):
        # update cuda architecture if necessary
        if '+cuda' in self.spec:
            cuda_arch = self.spec.variants['cuda_arch'].value
            archflag = '-arch=compute_{0}'.format(cuda_arch)

            filter_file('-arch compute_13', '',
                        'libhmsbeagle/GPU/kernels/Makefile.am',
                        string=True)

            filter_file(r'(NVCCFLAGS="-O3).*(")',
                        r'\1 {0}\2'.format(archflag), 'configure.ac')

            # point CUDA_LIBS to libcuda.so
            filter_file('-L$with_cuda/lib', '-L$with_cuda/lib64/stubs',
                        'configure.ac', string=True)

    def configure_args(self):
        args = [
            # Since spack will inject architecture flags turn off -march=native
            # when building libbeagle.
            '--disable-march-native',
        ]

        if '+cuda' in self.spec:
            args.append('--with-cuda=%s' % self.spec['cuda'].prefix)
        else:
            args.append('--without-cuda')

        return args
