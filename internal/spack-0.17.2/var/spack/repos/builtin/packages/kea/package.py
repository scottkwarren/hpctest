# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Kea(AutotoolsPackage):
    """Modern, open source DHCPv4 & DHCPv6 server."""

    homepage = "https://www.isc.org/kea/"
    url      = "https://downloads.isc.org/isc/kea/1.6.2/kea-1.6.2.tar.gz"

    version('1.6.2', sha256='2af7336027143c3e98d8d1d44165b2c2cbb0252a92bd88f6dd4d2c6adb69d7b5')

    depends_on('m4',       type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('log4cplus')
    depends_on('boost')
