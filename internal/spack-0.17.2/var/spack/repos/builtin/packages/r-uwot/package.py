# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RUwot(RPackage):
    """The Uniform Manifold Approximation and Projection (UMAP) Method for Dimensionality Reduction

    An implementation of the Uniform Manifold Approximation and Projection
    dimensionality reduction by McInnes et al. (2018) <arXiv:1802.03426>. It
    also provides means to transform new data and to carry out supervised
    dimensionality reduction. An implementation of the related LargeVis method
    of Tang et al. (2016) <arXiv:1602.00370> is also provided. This is a
    complete re-implementation in R (and C++, via the 'Rcpp' package): no
    Python installation is required. See the uwot website
    (<https://github.com/jlmelville/uwot>) for more documentation and
    examples."""

    homepage = "https://github.com/jlmelville/uwot"
    url      = "https://cloud.r-project.org/src/contrib/uwot_0.1.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/uwot"

    version('0.1.10', sha256='6ee1b6027bce679cd5a35f647f516a5b327632234bcf323c7f3d5b5e10807d23')
    version('0.1.3', sha256='4936e6922444cae8a71735e945b6bb0828a1012232eb94568054f78451c406d7')

    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-fnn', type=('build', 'run'))
    depends_on('r-rspectra', type=('build', 'run'))
    depends_on('r-rcppannoy@0.0.11:', type=('build', 'run'))
    depends_on('r-rcppannoy@0.0.17:', when='@0.1.10:', type=('build', 'run'))
    depends_on('r-irlba', type=('build', 'run'))
    depends_on('r-rcppprogress', type=('build', 'run'))
    depends_on('r-dqrng', type=('build', 'run'))
    depends_on('r-rcppparallel', when='@:0.1.3', type=('build', 'run'))
    depends_on('gmake', when='@:0.1.3', type='build')