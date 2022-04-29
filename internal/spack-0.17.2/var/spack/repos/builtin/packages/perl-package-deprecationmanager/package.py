# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlPackageDeprecationmanager(PerlPackage):
    """Manage deprecation warnings for your distribution"""

    homepage = "https://metacpan.org/pod/Package::DeprecationManager"
    url      = "http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/Package-DeprecationManager-0.17.tar.gz"

    version('0.17', sha256='1d743ada482b5c9871d894966e87d4c20edc96931bb949fb2638b000ddd6684b')
