# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlEvalClosure(PerlPackage):
    """Safely and cleanly create closures via string eval"""

    homepage = "https://metacpan.org/pod/Eval::Closure"
    url      = "http://search.cpan.org/CPAN/authors/id/D/DO/DOY/Eval-Closure-0.14.tar.gz"

    version('0.14', sha256='ea0944f2f5ec98d895bef6d503e6e4a376fea6383a6bc64c7670d46ff2218cad')
