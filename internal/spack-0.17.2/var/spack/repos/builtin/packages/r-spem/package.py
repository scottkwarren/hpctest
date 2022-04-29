# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSpem(RPackage):
    """S-system parameter estimation method

       This package can optimize the parameter in S-system models given time
       series data"""

    homepage = "https://bioconductor.org/packages/SPEM"
    git      = "https://git.bioconductor.org/packages/SPEM.git"

    version('1.30.0', commit='6b2eb64bfe6287846b1408297dd46dc772431031')
    version('1.24.0', commit='537ed19e466008f2972a246479b327c95177a99e')
    version('1.22.0', commit='fddb7cd1f81e47eae603724ea149c2adca5b3eb4')
    version('1.20.0', commit='b0e1049c61a35da00882d21026f4c1eb03b17517')
    version('1.18.0', commit='3ab425dd9889885eac328d26b73366a875cd250b')
    version('1.16.0', commit='9c0a96374086765db9c81e36a662999067fa4cc7')

    depends_on('r@2.15.1:', type=('build', 'run'))
    depends_on('r-rsolnp', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
