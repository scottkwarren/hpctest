# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xscope(AutotoolsPackage, XorgPackage):
    """XSCOPE -- a program to monitor X11/Client conversations."""

    homepage = "https://cgit.freedesktop.org/xorg/app/xscope"
    xorg_mirror_path = "app/xscope-1.4.1.tar.gz"

    version('1.4.1', sha256='f99558a64e828cd2c352091ed362ad2ef42b1c55ef5c01cbf782be9735bb6de3')

    depends_on('xproto@7.0.17:')
    depends_on('xtrans')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
