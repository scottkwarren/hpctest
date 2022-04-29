# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RLfe(RPackage):
    """Linear Group Fixed Effects

    Transforms away factors with many levels prior to doing an OLS. Useful for
    estimating linear models with multiple group fixed effects, and for
    estimating linear models which uses factors with many levels as pure
    control variables. See Gaure (2013) <doi:10.1016/j.csda.2013.03.024>
    Includes support for instrumental variables, conditional F statistics for
    weak instruments, robust and multi-way clustered standard errors, as well
    as limited mobility bias correction (Gaure 2014 <doi:10.1002/sta4.68>).
    WARNING: This package is NOT under active development anymore, no further
    improvements are to be expected, and the package is at risk of being
    removed from CRAN."""

    homepage = "https://cloud.r-project.org/package=lfe"
    url      = "https://cloud.r-project.org/src/contrib/lfe_2.8-5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/lfe"

    version('2.8-6', sha256='bf5fd362e9722e871a5236f30da562c489ae6506b667609b9465eefa8f101612')
    version('2.8-5', sha256='fd80c573d334594db933ff38f67bd4c9f899aaf648c3bd68f19477a0059723c2')
    version('2.8-4', sha256='ee5f6e312214aa73e285ae84a6bdf49ba10e830f1a68ffded2fea2e532f2cd6a')

    depends_on('r@2.15.2:', type=('build', 'run'))
    depends_on('r-matrix@1.1-2:', type=('build', 'run'))
    depends_on('r-formula', type=('build', 'run'))
    depends_on('r-xtable', type=('build', 'run'))
    depends_on('r-sandwich', type=('build', 'run'))
