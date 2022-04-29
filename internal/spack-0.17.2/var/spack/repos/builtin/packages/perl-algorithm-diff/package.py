# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlAlgorithmDiff(PerlPackage):
    """Compute 'intelligent' differences between two files / lists"""

    homepage = "https://metacpan.org/pod/Algorithm::Diff"
    url      = "http://search.cpan.org/CPAN/authors/id/T/TY/TYEMQ/Algorithm-Diff-1.1903.tar.gz"

    version('1.1903', sha256='30e84ac4b31d40b66293f7b1221331c5a50561a39d580d85004d9c1fff991751')
