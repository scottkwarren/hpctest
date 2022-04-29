# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPacman(RPackage):
    """Tools to more conveniently perform tasks associated with add-on
    packages. pacman conveniently wraps library and package related functions
    and names them in an intuitive and consistent fashion. It seeks to combine
    functionality from lower level functions which can speed up workflow."""

    homepage = "https://cloud.r-project.org/package=pacman"
    url      = "https://cloud.r-project.org/src/contrib/pacman_0.4.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/pacman"

    version('0.5.1', sha256='9ec9a72a15eda5b8f727adc877a07c4b36f8372fe7ed80a1bc6c2068dab3ef7c')
    version('0.5.0', sha256='61294757212ab0aa0153219d7d031f58be6f30ead88d84859001d58caa76603d')
    version('0.4.1', sha256='fffa72307912cbd5aa5bee0a9b65931500483036ccffb1791dd808eb5eb70362')

    depends_on('r@3.0.2:', type=('build', 'run'))
    depends_on('r@3.5.0:', when='@0.5.0:', type=('build', 'run'))
    depends_on('r-devtools', when='@:0.4.6', type=('build', 'run'))
    depends_on('r-remotes', when='@0.5.0:', type=('build', 'run'))
