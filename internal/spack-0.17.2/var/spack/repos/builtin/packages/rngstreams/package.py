# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Rngstreams(AutotoolsPackage):
    """Multiple independent streams of pseudo-random numbers."""

    homepage = "https://statmath.wu.ac.at/software/RngStreams"
    url      = "https://statmath.wu.ac.at/software/RngStreams/rngstreams-1.0.1.tar.gz"

    version('1.0.1', sha256='966195febb9fb9417e4e361948843425aee12efc8b4e85332acbcd011ff2d9b0')
