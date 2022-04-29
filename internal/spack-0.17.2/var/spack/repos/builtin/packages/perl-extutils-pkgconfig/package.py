# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlExtutilsPkgconfig(PerlPackage):
    """simplistic interface to pkg-config"""

    homepage = "https://metacpan.org/pod/ExtUtils::PkgConfig"
    url      = "http://search.cpan.org/CPAN/authors/id/X/XA/XAOC/ExtUtils-PkgConfig-1.16.tar.gz"

    version('1.16', sha256='bbeaced995d7d8d10cfc51a3a5a66da41ceb2bc04fedcab50e10e6300e801c6e')

    depends_on('pkgconfig', type=('build', 'run'))
