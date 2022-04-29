# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlSubIdentify(PerlPackage):
    """Retrieve names of code references"""

    homepage = "https://metacpan.org/pod/Sub::Identify"
    url      = "http://search.cpan.org/CPAN/authors/id/R/RG/RGARCIA/Sub-Identify-0.14.tar.gz"

    version('0.14', sha256='068d272086514dd1e842b6a40b1bedbafee63900e5b08890ef6700039defad6f')
