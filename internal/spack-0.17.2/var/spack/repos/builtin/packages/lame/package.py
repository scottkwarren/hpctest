# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lame(AutotoolsPackage):
    """LAME is a high quality MPEG Audio Layer III (MP3) encoder licensed
    under the LGPL."""

    homepage = "http://lame.sourceforge.net/"
    url      = "https://download.sourceforge.net/project/lame/lame/3.100/lame-3.100.tar.gz"

    version('3.100', sha256='ddfe36cab873794038ae2c1210557ad34857a4b6bdc515785d1da9e175b1da1e')

    depends_on('nasm', type='build')

    def configure_args(self):
        args = ['--enable-mp3rtp', '--disable-static']
        return args
