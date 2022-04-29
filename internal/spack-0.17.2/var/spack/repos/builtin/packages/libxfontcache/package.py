# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxfontcache(AutotoolsPackage, XorgPackage):
    """Xfontcache - X-TrueType font cache extension client library."""

    homepage = "https://cgit.freedesktop.org/xorg/lib/libXfontcache"
    xorg_mirror_path = "lib/libXfontcache-1.0.5.tar.gz"

    version('1.0.5', sha256='fdba75307a0983d2566554e0e9effa7079551f1b7b46e8de642d067998619659')

    depends_on('libx11')
    depends_on('libxext')

    depends_on('xextproto')
    depends_on('fontcacheproto')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
