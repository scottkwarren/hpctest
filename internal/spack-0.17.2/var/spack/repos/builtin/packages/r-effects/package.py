# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class REffects(RPackage):
    """Effect Displays for Linear, Generalized Linear, and Other Models

    Graphical and tabular effect displays, e.g., of interactions, for various
    statistical models with linear predictors."""

    cran     = "effects"

    version('4.2-0', sha256='6833dfbc65f3f33191a24e9b0d2aa0c964caeebb6c4fd2036ad94ed2723a7a46')

    depends_on('r@3.5.0:', type=('build', 'run'))
    depends_on('r-cardata', type=('build', 'run'))
    depends_on('r-lme4', type=('build', 'run'))
    depends_on('r-nnet', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-colorspace', type=('build', 'run'))
    depends_on('r-survey', type=('build', 'run'))
    depends_on('r-estimability', type=('build', 'run'))
    depends_on('r-insight', type=('build', 'run'))
