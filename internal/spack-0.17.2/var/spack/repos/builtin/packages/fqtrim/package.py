# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fqtrim(MakefilePackage):
    """fqtrim is a versatile stand-alone utility that can be used to trim
    adapters, poly-A tails, terminal unknown bases (Ns) and low quality 3'
    regions in reads from high-throughput next-generation sequencing
    machines."""

    homepage = "https://ccb.jhu.edu/software/fqtrim/"
    url      = "https://ccb.jhu.edu/software/fqtrim/dl/fqtrim-0.9.7.tar.gz"

    version('0.9.7', sha256='4951538f69dde14a23fc4841ff020434d26eb9622c4e06b43c068c702aa3d0d6')

    def build(self, spec, prefix):
        make('release')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('fqtrim', prefix.bin)
