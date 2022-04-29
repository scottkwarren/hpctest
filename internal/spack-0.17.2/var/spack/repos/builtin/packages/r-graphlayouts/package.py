# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGraphlayouts(RPackage):
    """Additional Layout Algorithms for Network Visualizations.

    Several new layout algorithms to visualize networks are provided which are
    not part of 'igraph'. Most are based on the concept of stress majorization
    by Gansner et al. (2004) <doi:10.1007/978-3-540-31843-9_25>. Some more
    specific algorithms allow to emphasize hidden group structures in networks
    or focus on specific nodes."""

    homepage = "https://github.com/schochastics/graphlayouts"
    url      = "https://cloud.r-project.org/src/contrib/graphlayouts_0.5.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/graphlayouts"

    version('0.7.1', sha256='380f8ccb0b08735694e83f661fd56a0d592a78448ae91b89c290ba8582d66717')
    version('0.5.0', sha256='83f61ce07580c5a64c7044c12b20d98ccf138c7e78ff12855cdfc206e1fab10d')

    depends_on('r@3.2.0:', type=('build', 'run'))
    depends_on('r-igraph', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-rcpparmadillo', type=('build', 'run'))
