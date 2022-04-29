# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cnmem(CMakePackage):
    """CNMem mempool for CUDA devices"""

    homepage = "https://github.com/NVIDIA/cnmem"
    git      = "https://github.com/NVIDIA/cnmem.git"

    version('git', branch='master')

    depends_on('cmake@2.8.8:', type='build')
