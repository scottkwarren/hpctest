# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBackcall(PythonPackage):
    """Specifications for callback functions passed in to an API"""

    homepage = "https://github.com/takluyver/backcall"
    pypi = "backcall/backcall-0.1.0.tar.gz"

    version('0.2.0', sha256='5cbdbf27be5e7cfadb448baf0aa95508f91f2bbc6c6437cd9cd06e2a4c215e1e')
    version('0.1.0', sha256='38ecd85be2c1e78f77fd91700c76e14667dc21e2713b63876c0eb901196e01e4')
