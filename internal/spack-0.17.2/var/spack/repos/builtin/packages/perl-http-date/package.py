# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlHttpDate(PerlPackage):
    """Date conversion routines"""

    homepage = "https://metacpan.org/pod/HTTP::Date"
    url      = "http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/HTTP-Date-6.02.tar.gz"

    version('6.02', sha256='e8b9941da0f9f0c9c01068401a5e81341f0e3707d1c754f8e11f42a7e629e333')
