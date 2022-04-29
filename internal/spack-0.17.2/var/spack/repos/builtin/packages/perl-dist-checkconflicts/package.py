# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlDistCheckconflicts(PerlPackage):
    """Declare version conflicts for your dist"""

    homepage = "https://metacpan.org/pod/Dist::CheckConflicts"
    url      = "http://search.cpan.org/CPAN/authors/id/D/DO/DOY/Dist-CheckConflicts-0.11.tar.gz"

    version('0.11', sha256='ea844b9686c94d666d9d444321d764490b2cde2f985c4165b4c2c77665caedc4')
