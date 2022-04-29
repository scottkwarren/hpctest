# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlPerlVersion(PerlPackage):
    """Parse and manipulate Perl version strings"""

    homepage = "https://metacpan.org/pod/Perl::Version"
    url      = "http://search.cpan.org/CPAN/authors/id/B/BD/BDFOY/Perl-Version-1.013_03.tar.gz"

    version('1.013_03', sha256='6b5978f598dcdf8a304500c1b7bcdce967ca05e7b38673cebfdb4237531c2ff9')

    depends_on('perl-file-slurp-tiny', type=('build', 'run'))
