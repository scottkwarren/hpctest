# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPypeg2(PythonPackage):
    """A PEG Parser-Interpreter in Python"""

    homepage = "https://fdik.org/pyPEG2/"
    pypi = "pypeg2/pyPEG2-2.15.2.tar.gz"

    version('2.15.2', sha256='2b2d4f80d8e1a9370b2a91f4a25f4abf7f69b85c8da84cd23ec36451958a1f6d')

    depends_on('py-lxml', type=('build', 'run'))
