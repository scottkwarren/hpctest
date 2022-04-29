# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlIoSessiondata(PerlPackage):
    """A wrapper around a single IO::Socket object"""

    homepage = "https://metacpan.org/release/PHRED/IO-SessionData-1.03/source/lib/IO/SessionData.pm#PIO::SessionData"
    url      = "http://search.cpan.org/CPAN/authors/id/P/PH/PHRED/IO-SessionData-1.03.tar.gz"

    version('1.03', sha256='64a4712a3edbb3fd10230db296c29c8c66f066adfbc0c3df6a48258fef392ddd')
