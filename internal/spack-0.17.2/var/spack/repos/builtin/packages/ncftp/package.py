# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ncftp(AutotoolsPackage):
    """NcFTP Client is a set of application programs implementing the
       File Transfer Protocol."""

    homepage = "https://www.ncftp.com/"
    url      = "ftp://ftp.ncftp.com/ncftp/ncftp-3.2.6-src.tar.gz"

    version('3.2.6', sha256='129e5954850290da98af012559e6743de193de0012e972ff939df9b604f81c23')

    depends_on('ncurses')
