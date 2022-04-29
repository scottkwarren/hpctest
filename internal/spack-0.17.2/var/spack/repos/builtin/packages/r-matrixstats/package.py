# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMatrixstats(RPackage):
    """Functions that Apply to Rows and Columns of Matrices (and to Vectors)

    High-performing functions operating on rows and columns of matrices, e.g.
    col / rowMedians(), col / rowRanks(), and col / rowSds(). Functions
    optimized per data type and for subsetted calculations such that both
    memory usage and processing time is minimized. There are also optimized
    vector-based methods, e.g. binMeans(), madDiff() and weightedMedian()."""

    homepage = "https://cloud.r-project.org/package=matrixStats"
    cran = "matrixStats"

    version('0.61.0', sha256='dbd3c0ec59b1ae62ff9b4c2c90c4687cbd680d1796f6fdd672319458d4d2fd9a')
    version('0.58.0', sha256='8367b4b98cd24b6e40022cb2b11e907aa0bcf5ee5b2f89fefb186f53661f4b49')
    version('0.57.0', sha256='f9681887cd3b121762c83f55f189cae26cb8443efce91fcd212ac714fde9f343')
    version('0.55.0', sha256='16d6bd90eee4cee8df4c15687de0f9b72730c03e56603c2998007d4533e8db19')
    version('0.54.0', sha256='8f0db4e181300a208b9aedbebfdf522a2626e6675d2662656efb8ba71b05a06f')
    version('0.52.2', sha256='39da6aa6b109f89a141dab8913d981abc4fbd3f8be9e206f92e382cc5270d2a5')

    depends_on('r@2.12.0:', type=('build', 'run'))
