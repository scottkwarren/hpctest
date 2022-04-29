# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xclip(AutotoolsPackage):
    """xclip is a command line utility that is designed to run on any system
       with an X11 implementation. It provides an interface to X selections
       ("the clipboard") from the command line. It can read data from standard
       in or a file and place it in an X selection for pasting into other X
       applications. xclip can also print an X selection to standard out,
       which can then be redirected to a file or another program."""

    homepage = "https://github.com/astrand/xclip"
    git      = "https://github.com/astrand/xclip.git"

    version('0.13', commit='9aa7090c3b8b437c6489edca32ae43d82e0c1281')

    depends_on('libxmu')
    depends_on('libx11')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')
