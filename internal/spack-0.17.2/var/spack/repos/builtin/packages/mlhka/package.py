# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mlhka(Package):
    """A maximum likelihood ratio test of natural selection, using polymorphism
       and divergence data."""

    homepage = "https://wright.eeb.utoronto.ca"
    git      = "https://github.com/rossibarra/MLHKA.git"

    version('2.1', commit='e735ddd39073af58da21b00b27dea203736e5467')

    def install(self, spec, prefix):
        cxx = which('c++')
        cxx('MLHKA_version{0}.cpp'.format(self.version), '-o', 'MLHKA')
        mkdirp(prefix.bin)
        install('MLHKA', prefix.bin)
