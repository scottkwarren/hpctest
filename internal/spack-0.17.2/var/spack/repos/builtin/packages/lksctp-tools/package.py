# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class LksctpTools(AutotoolsPackage):
    """A Linux SCTP helper library"""

    homepage = "https://github.com/sctp/lksctp-tools"
    url      = "https://github.com/sctp/lksctp-tools/archive/v1.0.18.tar.gz"

    version('1.0.18', sha256='3e9ab5b3844a8b65fc8152633aafe85f406e6da463e53921583dfc4a443ff03a')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
