# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Rendercheck(AutotoolsPackage, XorgPackage):
    """rendercheck is a program to test a Render extension implementation
    against separate calculations of expected output."""

    homepage = "https://cgit.freedesktop.org/xorg/app/rendercheck"
    xorg_mirror_path = "app/rendercheck-1.5.tar.gz"

    version('1.5', sha256='1553fef61c30f2524b597c3758cc8d3f8dc1f52eb8137417fa0667b0adc8a604')

    depends_on('libxrender')
    depends_on('libx11')

    depends_on('xproto@7.0.17:')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
