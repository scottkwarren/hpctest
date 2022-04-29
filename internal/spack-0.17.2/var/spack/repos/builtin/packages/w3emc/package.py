# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class W3emc(CMakePackage):
    """This library contains Fortran 90 decoder/encoder routines for GRIB
    edition 1 with EMC changes.

    This is part of the NCEPLIBS project."""

    homepage = "https://noaa-emc.github.io/NCEPLIBS-w3emc/"
    url      = "https://github.com/NOAA-EMC/NCEPLIBS-w3emc/archive/refs/tags/v2.9.0.tar.gz"

    maintainers = ['t-brown', 'kgerheiser', 'Hang-Lei-NOAA', 'edwardhartnett']

    version('2.9.2', sha256='eace811a1365f69b85fdf2bcd93a9d963ba72de5a7111e6fa7c0e6578b69bfbc')
    version('2.9.1', sha256='d3e705615bdd0b76a40751337d943d5a1ea415636f4e5368aed058f074b85df4')
    version('2.9.0', sha256='994f59635ab91e34e96cab5fbaf8de54389d09461c7bac33b3104a1187e6c98a')
    version('2.7.3', sha256='eace811a1365f69b85fdf2bcd93a9d963ba72de5a7111e6fa7c0e6578b69bfbc')

    depends_on('bacio', when='@2.9.2:')

    # w3emc 2.7.3 contains gblevents which has these dependencies
    depends_on('nemsio', when='@2.7.3')
    depends_on('sigio', when='@2.7.3')
    depends_on('netcdf-fortran', when='@2.7.3')
