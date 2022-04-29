# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dcap(AutotoolsPackage):
    """dCache access protocol client library."""

    homepage = "https://github.com/dCache/dcap"
    url      = "https://github.com/dCache/dcap/archive/2.47.12.tar.gz"

    version('2.47.12', sha256='050a8d20c241abf358d5d72586f9abc43940e61d9ec9480040ac7da52ec804ac')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./bootstrap.sh')
