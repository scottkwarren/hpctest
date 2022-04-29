# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Shark(CMakePackage):
    """Shark is a fast, modular, general open-source C++ machine
    learning library. """

    homepage = "https://www.shark-ml.org/"
    url      = "https://github.com/Shark-ML/Shark/archive/v4.0.1.tar.gz"

    version('4.0.1', sha256='1caf9c73c5ebf54f9543a090e2b05ac646f95559aa1de483cd7662c378c1ec21')
    version('4.0.0', sha256='19d4099776327d5f8a2e2be286818c6081c61eb13ca279c1e438c86e70d90210')
    version('3.1.4', sha256='160c35ddeae3f6aeac3ce132ea4ba2611ece39eee347de2faa3ca52639dc6311')

    depends_on('boost')

    def cmake_args(self):
        args = ["-DBoost_USE_STATIC_LIBS=ON", "-DBOOST_ROOT={0}".format(
            self.spec['boost'].prefix)]
        return args
