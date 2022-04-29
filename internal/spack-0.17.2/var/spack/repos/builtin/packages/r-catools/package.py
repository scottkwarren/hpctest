# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RCatools(RPackage):
    """Tools: Moving Window Statistics, GIF, Base64, ROC AUC, etc

    Contains several basic utility functions including: moving (rolling,
    running) window statistic functions, read/write for GIF and ENVI binary
    files, fast calculation of AUC, LogitBoost classifier, base64
    encoder/decoder, round-off-error-free sum and cumsum, etc."""

    homepage = "https://cloud.r-project.org/package=caTools"
    url      = "https://cloud.r-project.org/src/contrib/caTools_1.17.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/caTools"

    version('1.18.1', sha256='ffeba4ffbeed5d491bf79b1fde3477f413341e412f77316af20439f54447c9f9')
    version('1.17.1.2', sha256='69cc542fab5677462b1a768709d0c4a0a0790f5db53e1fe9ae7123787c18726b')
    version('1.17.1.1', sha256='d53e2c5c77f1bd4744703d7196dbc9b4671a120bbb5b9b3edc45fc57c0650c06')
    version('1.17.1', sha256='d32a73febf00930355cc00f3e4e71357412e0f163faae6a4bf7f552cacfe9af4')

    depends_on('r@2.2.0:', type=('build', 'run'))
    depends_on('r@3.6.0:', when='@1.18.1:', type=('build', 'run'))
    depends_on('r-bitops', type=('build', 'run'))
