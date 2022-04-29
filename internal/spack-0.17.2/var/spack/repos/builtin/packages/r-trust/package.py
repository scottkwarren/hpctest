# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTrust(RPackage):
    """Trust Region Optimization

    Does local optimization using two derivatives and trust regions.
    Guaranteed to converge to local minimum of objective function."""

    homepage = "https://www.stat.umn.edu/geyer/trust"
    url      = "https://cloud.r-project.org/src/contrib/trust_0.1-7.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/trust"

    version('0.1-8', sha256='952e348b62aec35988b103fd152329662cb6a451538f184549252fbf49d7dcac')
    version('0.1-7', sha256='e3d15aa84a71becd2824253d4a8156bdf1ab9ac3b72ced0cd53f3bb370ac6f04')

    depends_on('r@2.10.0:', type=('build', 'run'))
