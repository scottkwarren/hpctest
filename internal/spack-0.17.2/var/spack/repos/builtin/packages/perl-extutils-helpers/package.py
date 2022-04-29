# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlExtutilsHelpers(PerlPackage):
    """ExtUtils::Helpers - Various portability utilities for module builders"""

    homepage = "https://metacpan.org/pod/ExtUtils::Helpers"
    url      = "https://cpan.metacpan.org/authors/id/L/LE/LEONT/ExtUtils-Helpers-0.026.tar.gz"

    version('0.026', sha256='de901b6790a4557cf4ec908149e035783b125bf115eb9640feb1bc1c24c33416')
