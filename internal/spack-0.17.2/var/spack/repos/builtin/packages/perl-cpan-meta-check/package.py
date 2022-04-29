# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlCpanMetaCheck(PerlPackage):
    """This module verifies if requirements described in a CPAN::Meta object
       are present.."""

    homepage = "https://metacpan.org/pod/CPAN::Meta::Check"
    url      = "http://search.cpan.org/CPAN/authors/id/L/LE/LEONT/CPAN-Meta-Check-0.014.tar.gz"

    version('0.014', sha256='28a0572bfc1c0678d9ce7da48cf521097ada230f96eb3d063fcbae1cfe6a351f')

    depends_on('perl-test-deep', type=('build', 'run'))
