# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCombinat(RPackage):
    """routines for combinatorics"""

    homepage = "https://cloud.r-project.org/package=combinat"
    url      = "https://cloud.r-project.org/src/contrib/combinat_0.0-8.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/combinat/"

    version('0.0-8', sha256='1513cf6b6ed74865bfdd9f8ca58feae12b62f38965d1a32c6130bef810ca30c1')
