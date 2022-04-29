# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Exampm(CMakePackage):
    """Exascale Material Point Method (MPM) Mini-App"""

    homepage = "https://github.com/ECP-copa/ExaMPM"
    git      = "https://github.com/ECP-copa/ExaMPM.git"

    maintainers = ["junghans", "streeve", "sslattery"]

    tags = ['proxy-app', 'ecp-proxy-app']

    version('master', branch='master')

    variant('shared', default=True, description='Build shared libraries')

    depends_on('mpi')
    depends_on('kokkos@3.0:')
    depends_on('silo')
    depends_on('cabana+mpi@master')

    def cmake_args(self):
        options = [
            '-DBUILD_SHARED_LIBS=%s' % (
                'On' if '+shared'  in self.spec else 'Off')
        ]

        return options
