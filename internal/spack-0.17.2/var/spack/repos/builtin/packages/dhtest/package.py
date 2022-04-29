# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dhtest(MakefilePackage):
    """dhtest linux dhcp client simulation tool. It can simulate
    hundreds of dhcp client from a linux machine. Linux root login
    is needed because the tool requires layer2 raw socket for sending
    and receiving dhcp packets."""

    homepage = "https://github.com/saravana815/dhtest"
    url      = "https://github.com/saravana815/dhtest/archive/v1.5.tar.gz"

    version('1.5', sha256='df66150429a59a3b6cea9b29e2687707d04ab10db5dfe1c893ba3e0b0531b151')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('dhtest', prefix.bin)
