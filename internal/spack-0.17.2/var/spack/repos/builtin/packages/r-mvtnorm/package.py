# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMvtnorm(RPackage):
    """Multivariate Normal and t Distributions

    Computes multivariate normal and t probabilities, quantiles, random
    deviates and densities."""

    homepage = "https://mvtnorm.r-forge.r-project.org/"
    cran = "mvtnorm"

    version('1.1-3', sha256='ff4e302139ba631280fc9c4a2ab168596bfd09e17a805974199b043697c02448')
    version('1.1-1', sha256='e965dad5e93babb7ded25b5ebdbd52332191b61f897d68853a379a07620d45de')
    version('1.0-11', sha256='0321612de99aa9bc75a45c7e029d3372736014223cbdefb80d8cae600cbc7252')
    version('1.0-10', sha256='31df19cd8b4cab9d9a70dba00442b7684e625d4ca143a2c023c2c5872b07ad12')
    version('1.0-6', sha256='4a015b57b645b520151b213eb04b7331598c06442a3f652c7dc149425bd2e444')
    version('1.0-5', sha256='d00f9f758f0d0d4b999f259223485dc55d23cbec09004014816f180045ac81dd')

    depends_on('r@1.9.0:', when='@:1.0-8', type=('build', 'run'))
    depends_on('r@3.5.0:', when='@1.0-9:', type=('build', 'run'))
