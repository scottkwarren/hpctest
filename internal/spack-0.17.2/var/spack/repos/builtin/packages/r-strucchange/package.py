# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RStrucchange(RPackage):
    """Testing, Monitoring, and Dating Structural Changes

    Testing, monitoring and dating structural changes in (linear) regression
    models. strucchange features tests/methods from the generalized fluctuation
    test framework as well as from the F test (Chow test) framework. This
    includes methods to fit, plot and test fluctuation processes (e.g., CUSUM,
    MOSUM, recursive/moving estimates) and F statistics, respectively. It is
    possible to monitor incoming data online using fluctuation processes.
    Finally, the breakpoints in regression models with structural changes can
    be estimated together with confidence intervals. Emphasis is always given
    to methods for visualizing the data."""

    homepage = "https://cloud.r-project.org/package=strucchange"
    url      = "https://cloud.r-project.org/src/contrib/strucchange_1.5-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/strucchange"

    version('1.5-2', sha256='7d247c5ae6f5a63c80e478799d009c57fb8803943aa4286d05f71235cc1002f8')
    version('1.5-1', sha256='740e2e20477b9fceeef767ae1002adc5ec397cb0f7daba5289a2c23b0dddaf31')

    depends_on('r@2.10.0:', type=('build', 'run'))
    depends_on('r-zoo', type=('build', 'run'))
    depends_on('r-sandwich', type=('build', 'run'))
