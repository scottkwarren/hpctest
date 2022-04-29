# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Httpress(MakefilePackage):
    """High performance HTTP server stress & benchmark utility."""

    homepage = "https://bitbucket.org/yarosla/httpress/wiki/Home"
    hg       = "https://bitbucket.org/yarosla/httpress"

    version('develop')
    version('1.1.0', revision='1.1.0')

    depends_on('mercurial', type='build')
    depends_on('libev')
    depends_on('gnutls')

    def install(self, spec, prefix):
        install_tree('./bin/Release', prefix.bin)
        install_tree('./obj/Release', prefix.obj)
