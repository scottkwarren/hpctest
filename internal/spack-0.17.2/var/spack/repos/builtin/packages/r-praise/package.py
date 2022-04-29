# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPraise(RPackage):
    """Build friendly R packages that praise their users if they have done
    something good, or they just need it to feel better."""

    homepage = "https://github.com/gaborcsardi/praise"
    url      = "https://cloud.r-project.org/src/contrib/praise_1.0.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/praise"

    version('1.0.0', sha256='5c035e74fd05dfa59b03afe0d5f4c53fbf34144e175e90c53d09c6baedf5debd')
