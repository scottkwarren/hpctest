# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlDigestMd5(PerlPackage):
    """Perl interface to the MD5 Algorithm"""

    homepage = "https://metacpan.org/pod/Digest::MD5"
    url      = "http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/Digest-MD5-2.55.tar.gz"

    version('2.55', sha256='03b198a2d14425d951e5e50a885d3818c3162c8fe4c21e18d7798a9a179d0e3c')
