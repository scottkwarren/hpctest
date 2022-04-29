# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xhost(AutotoolsPackage, XorgPackage):
    """xhost is used to manage the list of host names or user names
    allowed to make connections to the X server."""

    homepage = "https://cgit.freedesktop.org/xorg/app/xhost"
    xorg_mirror_path = "app/xhost-1.0.7.tar.gz"

    version('1.0.7', sha256='8dd1b6245dfbdef45a64a18ea618f233f77432c2f30881b1db9dc40d510d9490')

    depends_on('libx11')
    depends_on('libxmu')
    depends_on('libxau')

    depends_on('xproto@7.0.22:')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
