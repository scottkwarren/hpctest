# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlRegexpCommon(PerlPackage):
    """Regexp::Common - Provide commonly requested regular expressions"""

    homepage = "https://metacpan.org/pod/Regexp::Common"
    url      = "https://cpan.metacpan.org/authors/id/A/AB/ABIGAIL/Regexp-Common-2017060201.tar.gz"

    version('2017060201', sha256='ee07853aee06f310e040b6bf1a0199a18d81896d3219b9b35c9630d0eb69089b')
