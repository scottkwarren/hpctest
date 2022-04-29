# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlDevelOverloadinfo(PerlPackage):
    """Returns information about overloaded operators for a given class"""

    homepage = "https://metacpan.org/pod/Devel::OverloadInfo"
    url      = "http://search.cpan.org/CPAN/authors/id/I/IL/ILMARI/Devel-OverloadInfo-0.004.tar.gz"

    version('0.005', sha256='8bfde2ffa47c9946f8adc8cfc445c2f97b8d1cdd678111bee9f444e82f7aa6e7')
    version('0.004', sha256='83e88450064b0b0bbfd520cc9d7997fc7bed14ae257894eeadda28dc3e94937d')

    depends_on('perl-mro-compat', type=('build', 'run'))
