# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RClustergeneration(RPackage):
    """Random Cluster Generation (with Specified Degree of Separation)

    We developed the clusterGeneration package to provide functions  for
    generating random clusters, generating random  covariance/correlation
    matrices, calculating a separation index (data and population version) for
    pairs of clusters or cluster distributions, and 1-D and 2-D projection
    plots to visualize clusters.  The package also contains a function to
    generate random clusters based on factorial designs with factors such as
    degree of separation, number of clusters, number of variables, number of
    noisy variables."""

    homepage = "https://cloud.r-project.org/package=clusterGeneration"
    url      = "https://cloud.r-project.org/src/contrib/clusterGeneration_1.3.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/clusterGeneration/"

    version('1.3.7', sha256='534f29d8f7ed11e6e9a496f15845b588ec7133f3da5e6def8140b88500e52d5c')
    version('1.3.4', sha256='7c591ad95a8a9d7fb0e4d5d80dfd78f7d6a63cf7d11eb53dd3c98fdfb5b868aa')

    depends_on('r@2.9.1:', type=('build', 'run'))
    depends_on('r@3.5.0:', when='@1.3.7:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
