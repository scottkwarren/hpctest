# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Numap(CMakePackage):
    """Numap is a Linux library dedicated to memory profiling based on
    hardware performance monitoring unit (PMU)."""

    homepage = "https://github.com/numap-library/numap"
    git      = "https://github.com/numap-library/numap.git"
    maintainers = ['trahay']

    version('master',  branch='master')
    version('2019-09-06', commit='ffcdb88c64b59b7a3220eb1077d2b237029ca96a')

    depends_on('libpfm4')
