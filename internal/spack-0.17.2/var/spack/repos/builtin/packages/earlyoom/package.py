# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Earlyoom(MakefilePackage):
    """The oom-killer generally has a bad reputation among Linux users."""

    homepage = "https://github.com/rfjakob/earlyoom"
    url      = "https://github.com/rfjakob/earlyoom/archive/v1.6.1.tar.gz"

    version('1.6.1', sha256='bcd3fab4da5e1dddec952a0974c866ec90c5f9159c995f9162c45488c4d03340')
    version('1.6',   sha256='b81804fc4470f996014d52252a87a1cf3b43d3d8754140035b10dcee349302b8')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('earlyoom', prefix.bin)
