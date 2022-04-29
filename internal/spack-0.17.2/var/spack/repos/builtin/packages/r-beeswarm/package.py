# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBeeswarm(RPackage):
    """beeswarm: The Bee Swarm Plot, an Alternative to Stripchart"""

    homepage = "https://www.cbs.dtu.dk/~eklund/beeswarm/"
    url      = "https://cloud.r-project.org/src/contrib/beeswarm_0.2.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/beeswarm"

    version('0.2.3', sha256='0115425e210dced05da8e162c8455526a47314f72e441ad2a33dcab3f94ac843')
