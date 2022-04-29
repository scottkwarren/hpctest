# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDelayedmatrixstats(RPackage):
    """Functions that Apply to Rows and Columns of 'DelayedMatrix' Objects

       A port of the 'matrixStats' API for use with DelayedMatrix objects from
       the 'DelayedArray' package. High-performing functions operating on rows
       and columns of DelayedMatrix objects, e.g. col / rowMedians(), col /
       rowRanks(), and col / rowSds(). Functions optimized per data type and
       for subsetted calculations such that both memory usage and processing
       time is minimized."""

    homepage = "https://github.com/PeteHaitch/DelayedMatrixStats"
    git      = "https://git.bioconductor.org/packages/DelayedMatrixStats.git"

    version('1.12.3', commit='2b3091dfa9b3bab914e3a4157182063714ba86ae')
    version('1.6.1', commit='4378d1898a403305a94b122c4f36d1215fa7708d')
    version('1.4.0', commit='eb5b390ef99651fe87a346848f807de95afe8971')
    version('1.2.0', commit='de868e730be6280dfad41a280ab09f4d3083c9ac')
    version('1.0.3', commit='e29a3444980ff727c5b12286884b06dfaebf5b5b')

    depends_on('r-matrixgenerics', when='@1.12.2:', type=('build', 'run'))
    depends_on('r-delayedarray', type=('build', 'run'))
    depends_on('r-delayedarray@0.5.27:', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-delayedarray@0.7.37:', when='@1.4.0:', type=('build', 'run'))
    depends_on('r-delayedarray@0.9.8:', when='@1.6.1:', type=('build', 'run'))
    depends_on('r-delayedarray@0.15.3:', when='@1.12.2:', type=('build', 'run'))
    depends_on('r-matrixstats@0.53.1:', type=('build', 'run'))
    depends_on('r-matrixstats@0.55.0:', when='@1.6.1:', type=('build', 'run'))
    depends_on('r-matrixstats@0.56.0:', when='@1.12.2:', type=('build', 'run'))
    depends_on('r-sparsematrixstats', when='@1.12.2:', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-s4vectors@0.17.5:', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-hdf5array@1.7.10:', when='@1.4.0:', type=('build', 'run'))
    depends_on('r-hdf5array@1.17.2:', when='@1.12.2:', type=('build', 'run'))
    depends_on('r-biocparallel', when='@1.4.0:', type=('build', 'run'))
