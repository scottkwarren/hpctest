# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fslsfonts(AutotoolsPackage, XorgPackage):
    """fslsfonts produces a list of fonts served by an X font server."""

    homepage = "https://cgit.freedesktop.org/xorg/app/fslsfonts"
    xorg_mirror_path = "app/fslsfonts-1.0.5.tar.gz"

    version('1.0.5', sha256='27e58d2313835ce0f08cf47c59a43798b122f605a55f54b170db27b57a492007')

    depends_on('libfs')

    depends_on('xproto@7.0.25:')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
