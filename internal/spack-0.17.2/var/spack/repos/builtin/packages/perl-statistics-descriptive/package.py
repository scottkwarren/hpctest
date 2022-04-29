# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlStatisticsDescriptive(PerlPackage):
    """Module of basic descriptive statistical functions."""

    homepage = "https://metacpan.org/pod/Statistics::Descriptive"
    url      = "http://search.cpan.org/CPAN/authors/id/S/SH/SHLOMIF/Statistics-Descriptive-3.0612.tar.gz"

    version('3.0612', sha256='772413148e5e00efb32f277c4254aa78b9112490a896208dcd0025813afdbf7a')
