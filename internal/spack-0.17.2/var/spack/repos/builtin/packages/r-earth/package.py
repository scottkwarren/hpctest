# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class REarth(RPackage):
    """Multivariate Adaptive Regression Splines.

    Build regression models using the techniques in Friedman's papers
    "Fast MARS" and "Multivariate Adaptive Regression Splines"
    <doi:10.1214/aos/1176347963>."""

    homepage = "http://www.milbo.users.sonic.net/earth"
    url      = "https://cloud.r-project.org/src/contrib/earth_5.1.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/earth"

    version('5.3.0', sha256='05ace806271a74b3ddf8718a93237fe2a8550a8659ebd87f8079c0bda5e02437')
    version('5.1.2', sha256='326f98e8c29365ca3cd5584cf2bd6529358f5ef81664cbd494162f92b6c3488d')

    depends_on('r@3.4.0:', type=('build', 'run'))
    depends_on('r-formula@1.2-3:', type=('build', 'run'))
    depends_on('r-plotmo@3.5.4:', type=('build', 'run'))
    depends_on('r-plotmo@3.6.0:', when='@5.3.0', type=('build', 'run'))
    depends_on('r-teachingdemos@2.10:', type=('build', 'run'))
