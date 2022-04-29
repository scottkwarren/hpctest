# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RZoo(RPackage):
    """S3 Infrastructure for Regular and Irregular Time Series (Z's Ordered Observations)

    An S3 class with methods for totally ordered indexed observations. It is
    particularly aimed at irregular time series of numeric vectors/matrices and
    factors. zoo's key design goals are independence of a particular
    index/date/time class and consistency with ts and base R by providing
    methods to extend standard generics."""

    homepage = "https://zoo.r-forge.r-project.org/"
    url      = "https://cloud.r-project.org/src/contrib/zoo_1.7-14.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/zoo"

    version('1.8-8', sha256='4e8cc4065047ba12e103b9664f3b607c770673096e9c2b694fad2b2ec3203ce7')
    version('1.8-6', sha256='2217a4f362f2201443b5fdbfd9a77d9a6caeecb05f02d703ee8b3b9bf2af37cc')
    version('1.8-5', sha256='8773969973d28d7d1a48f74b73be1dbd97acb3b22a4668a102e8bb585a7de826')
    version('1.7-14', sha256='4858675fed056a4329c4998517cc944db386447483390bd342de719e0509f598')
    version('1.7-13', sha256='0ca5264d6077c785963705e462aec3e57e0d0651379f9bf4ee32e4f3b25dc754')

    depends_on('r@2.10.0:', type=('build', 'run'))
    depends_on('r@3.1.0:', when='@1.8-2:', type=('build', 'run'))
    depends_on('r-lattice@0.20-27:', type=('build', 'run'))
