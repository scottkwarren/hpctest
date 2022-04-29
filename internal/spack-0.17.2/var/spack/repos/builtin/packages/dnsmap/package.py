# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dnsmap(MakefilePackage):
    """dnsmap was originally released back in 2006 and was inspired
    by the fictional story."""

    homepage = "https://github.com/makefu/dnsmap"
    git      = "https://github.com/makefu/dnsmap.git"

    version('master', branch='master')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('dnsmap', prefix.bin)
