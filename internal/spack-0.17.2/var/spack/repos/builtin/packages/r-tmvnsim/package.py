# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTmvnsim(RPackage):
    """Truncated Multivariate Normal Simulation

    Importance sampling from the truncated multivariate normal using the GHK
    (Geweke-Hajivassiliou-Keane) simulator. Unlike Gibbs sampling which can get
    stuck in one truncation sub-region depending on initial values, this
    package allows truncation based on disjoint regions that are created by
    truncation of absolute values. The GHK algorithm uses simple Cholesky
    transformation followed by recursive simulation of univariate truncated
    normals hence there are also no convergence issues. Importance sample is
    returned along with sampling weights, based on which, one can calculate
    integrals over truncated regions for multivariate normals."""

    homepage = "https://cloud.r-project.org/package=tmvnsim"
    url      = "https://cloud.r-project.org/src/contrib/tmvnsim_1.0-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/tmvnsim"

    version('1.0-2', sha256='97f63d0bab3b240cc7bdbe6e6e74e90ad25a4382a345ee51a26fe3959edeba0f')
