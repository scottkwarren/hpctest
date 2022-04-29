# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlFileWhich(PerlPackage):
    """Perl implementation of the which utility as an API"""

    homepage = "http://cpansearch.perl.org/src/PLICEASE/File-Which-1.22/lib/File/Which.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/P/PL/PLICEASE/File-Which-1.22.tar.gz"

    version('1.22', sha256='e8a8ffcf96868c6879e82645db4ff9ef00c2d8a286fed21971e7280f52cf0dd4')
