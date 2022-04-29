# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class RGoplot(RPackage):
    """Implementation of multilayered visualizations for enhanced graphical
       representation of functional analysis data. It combines and integrates
       omics data derived from expression and functional annotation enrichment
       analyses. Its plotting functions have been developed with an
       hierarchical structure in mind: starting from a general overview to
       identify the most enriched categories (modified bar plot, bubble plot)
       to a more detailed one displaying different types of relevant
       information for the molecules in a given set of categories
       (circle plot, chord plot, cluster plot, Venn diagram, heatmap)."""

    homepage = "https://github.com/wencke/wencke.github.io/issues"
    url      = "https://cloud.r-project.org/src/contrib/GOplot_1.0.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/GOplot"

    version('1.0.2', sha256='3ddaa2b6d1297ad6daad30d18af708adf43d86e8804b1b92fa29dfbf26d80df9')

    depends_on('r@3.2.3:', type=('build', 'run'))
    depends_on('r-ggplot2@2.0.0:', type=('build', 'run'))
    depends_on('r-ggdendro@0.1-17:', type=('build', 'run'))
    depends_on('r-gridextra@2.0.0:', type=('build', 'run'))
    depends_on('r-rcolorbrewer@1.1-2:', type=('build', 'run'))
