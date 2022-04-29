# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDiagrammer(RPackage):
    """Graph/Network Visualization

    Build graph/network structures using functions for stepwise addition and
    deletion of nodes and edges. Work with data available in tables for bulk
    addition of nodes, edges, and associated metadata. Use graph selections and
    traversals to apply changes to specific nodes or edges. A wide selection of
    graph algorithms allow for the analysis of graphs. Visualize the graphs and
    take advantage of any aesthetic properties assigned to nodes and edges."""

    homepage = "https://github.com/rich-iannone/DiagrammeR"
    url      = "https://cloud.r-project.org/src/contrib/DiagrammeR_0.8.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/DiagrammeR"

    version('1.0.6.1', sha256='be4e4c520a3692902ce405e8225aef9f3d5f0cd11fcde614f6541e981b63673d')
    version('1.0.1', sha256='ccee8acf608fc909e73c6de4374cef5a570cb62e5f454ac55dda736f22f3f013')
    version('1.0.0', sha256='2b186dae1b19018681b979e9444bf16559c42740d8382676fbaf3b0f8a44337e')
    version('0.8.4', sha256='0503935fa120c7c7cdcfd4dce85558b23fd0bcb7e6b32fa6989087d3c88ec404')

    depends_on('r@3.2.0:', when='@0.9.2:', type=('build', 'run'))
    depends_on('r-dplyr@0.7.4:', when='@1.0.0:', type=('build', 'run'))
    depends_on('r-dplyr@0.7.6:', when='@1.0.6.1:', type=('build', 'run'))
    depends_on('r-downloader@0.4:', when='@1.0.0:', type=('build', 'run'))
    depends_on('r-glue@1.2.0:', when='@1.0.0:', type=('build', 'run'))
    depends_on('r-glue@1.3.0:', when='@1.0.6.1:', type=('build', 'run'))
    depends_on('r-htmltools@0.3.6:', when='@1.0.0:', type=('build', 'run'))
    depends_on('r-htmlwidgets@1.0:', type=('build', 'run'))
    depends_on('r-htmlwidgets@1.2:', when='@1.0.6.1:', type=('build', 'run'))
    depends_on('r-igraph@1.1.2:', type=('build', 'run'))
    depends_on('r-igraph@1.2.2:', when='@1.0.6.1:', type=('build', 'run'))
    depends_on('r-influencer@0.1.0:', type=('build', 'run'))
    depends_on('r-magrittr@1.5:', when='@1.0.0:', type=('build', 'run'))
    depends_on('r-purrr@0.2.4:', when='@1.0.0:', type=('build', 'run'))
    depends_on('r-purrr@0.2.5:', when='@1.0.6.1:', type=('build', 'run'))
    depends_on('r-rcolorbrewer@1.1-2:', when='@1.0.0:', type=('build', 'run'))
    depends_on('r-readr@1.1.1:', when='@1.0.0:', type=('build', 'run'))
    depends_on('r-rlang@0.2.0:', when='@1.0.0:', type=('build', 'run'))
    depends_on('r-rlang@0.2.2:', when='@1.0.6.1:', type=('build', 'run'))
    depends_on('r-rstudioapi@0.7:', type=('build', 'run'))
    depends_on('r-scales@0.5.0:', type=('build', 'run'))
    depends_on('r-scales@1.0.0:', when='@1.0.6.1:', type=('build', 'run'))
    depends_on('r-stringr@1.3.0:', type=('build', 'run'))
    depends_on('r-stringr@1.3.1:', when='@1.0.6.1:', type=('build', 'run'))
    depends_on('r-tibble@1.4.2:', when='@1.0.0:', type=('build', 'run'))
    depends_on('r-tidyr@0.8.0:', when='@1.0.0:', type=('build', 'run'))
    depends_on('r-tidyr@0.8.1:', when='@1.0.6.1:', type=('build', 'run'))
    depends_on('r-viridis@0.5.0:', when='@1.0.0:', type=('build', 'run'))
    depends_on('r-viridis@0.5.1:', when='@1.0.6.1:', type=('build', 'run'))
    depends_on('r-visnetwork@2.0.3:', type=('build', 'run'))
    depends_on('r-visnetwork@2.0.4:', when='@1.0.6.1:', type=('build', 'run'))
    depends_on('r-rgexf@0.15.3:', when='@1.0.0:1.0.1', type=('build', 'run'))
