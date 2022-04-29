# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xset(AutotoolsPackage, XorgPackage):
    """User preference utility for X."""

    homepage = "https://cgit.freedesktop.org/xorg/app/xset"
    xorg_mirror_path = "app/xset-1.2.3.tar.gz"

    version('1.2.3', sha256='5ecb2bb2cbf3c9349b735080b155a08c97b314dacedfc558c7f5a611ee1297f7')

    depends_on('libxmu')
    depends_on('libx11')

    depends_on('xproto@7.0.17:')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
