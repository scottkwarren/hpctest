# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAnimation(RPackage):
    """Provides functions for animations in statistics, covering topics
    in probability theory, mathematical statistics, multivariate statistics,
    non-parametric statistics, sampling survey, linear models, time series,
    computational statistics, data mining and machine learning.
    These functions maybe helpful in teaching statistics and data analysis."""

    homepage = "https://cloud.r-project.org/package=animation"
    url = "https://cloud.r-project.org/src/contrib/animation_2.5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/animation"

    version('2.6', sha256='90293638920ac436e7e4de76ebfd92e1643ccdb0259b62128f16dd0b13245b0a')
    version('2.5', sha256='b232fef1b318c79710e5e1923d87baba4c85ffe2c77ddb188130e0911d8cb55f')

    depends_on('r+X', type=('build', 'run'))
    depends_on('r@2.14:', type=('build', 'run'))
    depends_on('r-magick', when='@2.6:', type=('build', 'run'))
    depends_on('imagemagick')
    depends_on('ffmpeg')
    depends_on('swftools')
    depends_on('texlive')
