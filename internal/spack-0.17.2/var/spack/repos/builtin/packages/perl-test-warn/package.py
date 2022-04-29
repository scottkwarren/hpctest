# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlTestWarn(PerlPackage):
    """Perl extension to test methods for warnings"""

    homepage = "https://metacpan.org/pod/Test::Warn"
    url      = "http://search.cpan.org/CPAN/authors/id/C/CH/CHORNY/Test-Warn-0.30.tar.gz"

    version('0.30', sha256='8197555b94189d919349a03f7058f83861f145af9bee59f505bfe47562144e41')
