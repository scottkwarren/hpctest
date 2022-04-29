# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sfcgal(CMakePackage):
    """
    SFCGAL is a C++ wrapper library around CGAL with the aim of supporting
    ISO 19107:2013 and OGC Simple Features Access 1.2 for 3D operations. SFCGAL
    provides standard compliant geometry types and operations, that can be
    accessed from its C or C++ APIs.
    """

    homepage = "http://www.sfcgal.org/"
    url      = "https://github.com/Oslandia/SFCGAL/archive/v1.3.8.tar.gz"

    version('1.3.8', sha256='5154bfc67a5e99d95cb653d70d2b9d9293d3deb3c8f18b938a33d68fec488a6d')
    version('1.3.7', sha256='30ea1af26cb2f572c628aae08dd1953d80a69d15e1cac225390904d91fce031b')

    depends_on('cmake@2.8.6:', type='build')
    # Ref: https://oslandia.github.io/SFCGAL/installation.html, but starts to work @4.7:
    depends_on('cgal@4.7: +core')
    depends_on('boost@1.54.0:')
    depends_on('mpfr@2.2.1:')
    depends_on('gmp@4.2:')

    def cmake_args(self):
        # It seems viewer is discontinued as of v1.3.0
        # https://github.com/Oslandia/SFCGAL/releases/tag/v1.3.0
        # Also, see https://github.com/Oslandia/SFCGAL-viewer
        return ['-DSFCGAL_BUILD_VIEWER=OFF']
