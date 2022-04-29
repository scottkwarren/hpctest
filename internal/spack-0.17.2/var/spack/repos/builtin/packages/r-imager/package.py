# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RImager(RPackage):
    """Image Processing Library Based on 'CImg'

    Fast image processing for images in up to 4 dimensions (two spatial
    dimensions, one time/depth dimension, one colour dimension). Provides most
    traditional image processing tools (filtering, morphology, transformations,
    etc.) as well as various functions for easily analysing image data using R.
    The package wraps 'CImg', <https://cimg.eu/>, a simple, modern C++ library
    for image processing."""

    homepage = "https://dahtah.github.io/imager"
    url      = "https://cloud.r-project.org/src/contrib/imager_0.41.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/imager"

    version('0.42.10', sha256='01939eb03ad2e1369a4240a128c3b246a4c56f572f1ea4967f1acdc555adaeee')
    version('0.42.3', sha256='6fc308153df8251cef48f1e13978abd5d29ec85046fbe0b27c428801d05ebbf3')
    version('0.41.2', sha256='9be8bc8b3190d469fcb2883045a404d3b496a0380f887ee3caea11f0a07cd8a5')

    depends_on('r+X')
    depends_on('r@2.10.0:', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-rcpp@0.11.5:', type=('build', 'run'))
    depends_on('r-stringr', type=('build', 'run'))
    depends_on('r-png', type=('build', 'run'))
    depends_on('r-jpeg', type=('build', 'run'))
    depends_on('r-readbitmap', type=('build', 'run'))
    depends_on('r-purrr', type=('build', 'run'))
    depends_on('r-downloader', type=('build', 'run'))
    depends_on('r-igraph', type=('build', 'run'))
    depends_on('r-cairo', when='@:0.41.2', type=('build', 'run'))
    depends_on('r-plyr', when='@:0.41.2', type=('build', 'run'))
    depends_on('fftw')
    depends_on('libtiff')
