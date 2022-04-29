# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lndir(AutotoolsPackage, XorgPackage):
    """lndir - create a shadow directory of symbolic links to another
    directory tree."""

    homepage = "https://cgit.freedesktop.org/xorg/util/lndir"
    xorg_mirror_path = "util/lndir-1.0.3.tar.gz"

    version('1.0.3', sha256='95b2d26fb3cbe702f828146c7a4c7c48001d2da52b062580227b7b68180be902')

    depends_on('xproto@7.0.17:')
    depends_on('pkgconfig', type='build')
