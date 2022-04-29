# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Rsbench(MakefilePackage):
    """A mini-app to represent the multipole resonance representation lookup
       cross section algorithm."""

    homepage = "https://github.com/ANL-CESAR/RSBench"
    url = "https://github.com/ANL-CESAR/RSBench/archive/v2.tar.gz"

    version('12', sha256='2e437dbdaf7bf12bb9ade429d46a9e74fd519fc4686777a452770790d0546499')
    version('2', sha256='1e97a38a863836e98cedc5cc669f8fdcaed905fafdc921d2bce32319b3e157ff')
    version('0', sha256='95c06cf4cb6f396f9964d5e4b58a477bf9d7131cd39804480f1cb74e9310b271')

    tags = ['proxy-app']

    # To-Do: Add build support for other parallelism versions in v12:
    # CUDA, Sycl, OpenCL, OpenMP Offload

    @property
    def build_directory(self):
        if self.spec.satisfies('@:2'):
            return 'src'
        return 'openmp-threading'

    @property
    def build_targets(self):
        targets = []

        cflags = '-std=gnu99 -O3'
        ldflags = '-lm'

        if self.compiler.name == 'gcc':
            cflags += ' -ffast-math '
        elif self.compiler.name == 'intel':
            cflags += ' -xhost -ansi-alias -no-prec-div '
        elif self.compiler.name == 'pgi' or self.compiler.name == 'nvhpc':
            cflags += ' -fastsse '
        elif self.compiler.name == 'arm':
            cflags += ' -ffast-math '

        cflags += self.compiler.openmp_flag

        targets.append('CFLAGS={0}'.format(cflags))
        targets.append('LDFLAGS={0}'.format(ldflags))

        return targets

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install(join_path(self.build_directory, 'rsbench'), prefix.bin)
