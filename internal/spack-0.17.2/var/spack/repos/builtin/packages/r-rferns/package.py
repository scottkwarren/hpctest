# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRferns(RPackage):
    """Random Ferns Classifier

    Provides the random ferns classifier by Ozuysal, Calonder, Lepetit and Fua
    (2009) <doi:10.1109/TPAMI.2009.23>, modified for generic and multi-label
    classification and featuring OOB error approximation and importance measure
    as introduced in Kursa (2014) <doi:10.18637/jss.v061.i10>."""

    homepage = "https://cloud.r-project.org/package=rFerns"
    url      = "https://cloud.r-project.org/src/contrib/rFerns_3.0.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rFerns"

    version('4.0.0', sha256='cc8cea0893390bf5db0fb0f59748d5bf6f29537d68bedca900268fd551489128')
    version('3.0.0', sha256='35e7e31a6497e415a0fe578678cf9b2f537b21319e4c015a1e2dade00310227c')
