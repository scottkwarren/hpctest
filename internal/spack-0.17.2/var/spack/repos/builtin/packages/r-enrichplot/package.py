# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class REnrichplot(RPackage):
    """Visualization of Functional Enrichment Result

       The 'enrichplot' package implements several visualization methods for
       interpreting functional enrichment results obtained from ORA or GSEA
       analysis. All the visualization methods are developed based on 'ggplot2'
       graphics."""

    homepage = "https://bioconductor.org/packages/enrichplot"
    git      = "https://git.bioconductor.org/packages/enrichplot.git"

    version('1.10.2', commit='77ee04f60a07cc31151f8f47f8ee64f3a43c9760')
    version('1.4.0', commit='6ffe5d9c5dbe5cbea29f2e0941595475bbbcea0e')
    version('1.2.0', commit='2eeaafb571d35a106eba8ae7df014f3201066e8b')
    version('1.0.2', commit='ba7726fa0d4b581b7514dcbb04889cdbdd75ff29')

    depends_on('r@3.4.0:', type=('build', 'run'))
    depends_on('r@3.5.0:', when='@1.10.2:', type=('build', 'run'))
    depends_on('r-cowplot', type=('build', 'run'))
    depends_on('r-dose', type=('build', 'run'))
    depends_on('r-dose@3.5.1:', when='@:1.4.0', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-ggraph', type=('build', 'run'))
    depends_on('r-igraph', type=('build', 'run'))
    depends_on('r-plyr', when='@1.10.2:', type=('build', 'run'))
    depends_on('r-purrr', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-rcolorbrewer', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-reshape2', type=('build', 'run'))
    depends_on('r-scatterpie', when='@1.10.2:', type=('build', 'run'))
    depends_on('r-shadowtext', when='@1.10.2:', type=('build', 'run'))
    depends_on('r-gosemsim', type=('build', 'run'))
    depends_on('r-magrittr', when='@1.10.2:', type=('build', 'run'))
    depends_on('r-ggridges', when='@:1.4.0', type=('build', 'run'))
    depends_on('r-upsetr', when='@:1.4.0', type=('build', 'run'))
    depends_on('r-annotationdbi', when='@:1.4.0', type=('build', 'run'))
    depends_on('r-europepmc', when='@1.2.0:1.4.0', type=('build', 'run'))
    depends_on('r-ggplotify', when='@1.2.0:1.4.0', type=('build', 'run'))
    depends_on('r-gridextra', when='@1.2.0:1.4.0', type=('build', 'run'))
