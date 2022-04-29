# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDendextend(RPackage):
    """Extending 'Dendrogram' Functionality in R

    Offers a set of functions for extending 'dendrogram' objects in R, letting
    you visualize and compare trees of 'hierarchical clusterings'. You can (1)
    Adjust a tree's graphical parameters - the color, size, type, etc of its
    branches, nodes and labels. (2) Visually and statistically compare
    different 'dendrograms' to one another."""

    homepage = "https://cloud.r-project.org/package=dendextend"
    url      = "https://cloud.r-project.org/src/contrib/dendextend_1.5.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/dendextend"

    version('1.14.0', sha256='3789461bc474e146b077ad26566b1fa05be32fc7e57ab1fb5e78bdabcc797858')
    version('1.12.0', sha256='b487fed8c1878a23b9e28394ee11f16a1831b76c90793eb486e6963c7162fa55')
    version('1.10.0', sha256='88f0fb3362d69144daf4f35d0ea09f32c2df1adf614e040327a42552a8fd3224')
    version('1.5.2', sha256='8228cf9cfd31ec30038aaa61a35959179bad748582d796999cd9ad78152a5f12')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-magrittr@1.0.1:', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-viridis', type=('build', 'run'))
    depends_on('r-fpc', when='@:1.10.0', type=('build', 'run'))
    depends_on('r-whisker', when='@:1.5.2', type=('build', 'run'))
