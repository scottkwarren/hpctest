# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libnova(AutotoolsPackage):
    """"libnova is a general purpose, double precision, Celestial Mechanics,
        Astrometry and Astrodynamics library."""

    homepage = "http://libnova.sourceforge.net"
    url      = "https://sourceforge.net/projects/libnova/files/libnova/v%200.15.0/libnova-0.15.0.tar.gz/download"

    version('0.15.0', sha256='7c5aa33e45a3e7118d77df05af7341e61784284f1e8d0d965307f1663f415bb1')

    depends_on('m4')
    depends_on('autoconf')
    depends_on('automake')
    depends_on('libtool')

    force_autoreconf = True
