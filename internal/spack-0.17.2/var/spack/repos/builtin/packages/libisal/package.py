# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libisal(AutotoolsPackage):
    """ISA-L is a collection of optimized low-level functions targeting
    storage applications."""

    homepage = "https://github.com/intel/isa-l"
    url      = "https://github.com/intel/isa-l/archive/v2.29.0.tar.gz"

    version('2.29.0', sha256='832d9747ef3f0c8c05d39e3d7fd6ee5299a844e1ee7382fc8c8b52a268f36eda')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    depends_on('nasm', type='build')

    def autoreconf(self, spec, prefix):
        autogen = Executable('./autogen.sh')
        autogen()
