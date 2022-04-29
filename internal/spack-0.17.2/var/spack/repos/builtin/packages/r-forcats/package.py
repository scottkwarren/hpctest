# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RForcats(RPackage):
    """Tools for Working with Categorical Variables (Factors)

    Helpers for reordering factor levels (including moving specified levels to
    front, ordering by first appearance, reversing, and randomly shuffling),
    and tools for modifying factor levels (including collapsing rare levels
    into other, 'anonymising', and manually 'recoding')."""

    homepage = "https://forcats.tidyverse.org/"
    cran = "forcats"

    version('0.5.1', sha256='c4fb96e874e2bedaa8a1aa32ea22abdee7906d93b5c5c7b42c0894c0c5b6a289')
    version('0.5.0', sha256='8f960e789333ec597ddf2d653a64e330f03b86f465e9b71f6779f227355d90c4')
    version('0.4.0', sha256='7c83cb576aa6fe1379d7506dcc332f7560068b2025f9e3ab5cd0a5f28780d2b2')
    version('0.3.0', sha256='95814610ec18b8a8830eba63751954387f9d21400d6ab40394ed0ff22c0cb657')
    version('0.2.0', sha256='b5bce370422d4c0ec9509249ae645373949bfbe9217cdf50dce2bfbdad9f7cd7')

    depends_on('r@3.1:', type=('build', 'run'))
    depends_on('r@3.2:', when='@0.5.0:', type=('build', 'run'))
    depends_on('r-ellipsis', when='@0.4.0:', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-rlang', when='@0.4.0:', type=('build', 'run'))
    depends_on('r-tibble', type=('build', 'run'))
