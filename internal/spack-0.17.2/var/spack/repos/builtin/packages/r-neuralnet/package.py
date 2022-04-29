# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RNeuralnet(RPackage):
    """Training of neural networks using backpropagation, resilient
    backpropagation with (Riedmiller, 1994) or without weight backtracking
    (Riedmiller and Braun, 1993) or the modified globally convergent version by
    Anastasiadis et al. (2005). The package allows flexible settings through
    custom-choice of error and activation function. Furthermore, the calculation of
    generalized weights (Intrator O & Intrator N, 1993) is implemented."""

    homepage = "https://cloud.r-project.org/package=neuralnet"
    url      = "https://cloud.r-project.org/src/contrib/neuralnet_1.44.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/neuralnet"

    version('1.44.2', sha256='5f66cd255db633322c0bd158b9320cac5ceff2d56f93e4864a0540f936028826')

    depends_on('r@2.9.0:', type=('build', 'run'))
    depends_on('r-mass',   type=('build', 'run'))
    depends_on('r-deriv',  type=('build', 'run'))
