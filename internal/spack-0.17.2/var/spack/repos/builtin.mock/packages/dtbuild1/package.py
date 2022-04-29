# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dtbuild1(Package):
    """Package for use as a build tool for deptypes testing which has its own
    deptree"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/dtbuild1-1.0.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef')

    depends_on('dtbuild2', type='build')
    depends_on('dtlink2')
    depends_on('dtrun2', type='run')
