# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RNada(RPackage):
    """Nondetects and Data Analysis for Environmental Data

    Contains methods described by Dennis Helsel in his book "Nondetects And
    Data Analysis: Statistics for Censored Environmental Data"."""

    homepage = "https://cloud.r-project.org/package=NADA"
    url      = "https://cloud.r-project.org/src/contrib/NADA_1.6-1.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/NADA"

    version('1.6-1.1', sha256='670ff6595ba074ed0a930b7a09624d5ef20616379a20e768c1a7b37332aee44a')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-survival', type=('build', 'run'))
