# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libedit(AutotoolsPackage):
    """An autotools compatible port of the NetBSD editline library"""
    homepage = "https://thrysoee.dk/editline/"
    url      = "https://thrysoee.dk/editline/libedit-20170329-3.1.tar.gz"

    version('3.1-20210216', sha256='2283f741d2aab935c8c52c04b57bf952d02c2c02e651172f8ac811f77b1fc77a')
    version('3.1-20191231', sha256='dbb82cb7e116a5f8025d35ef5b4f7d4a3cdd0a3909a146a39112095a2d229071')
    version('3.1-20170329', sha256='91f2d90fbd2a048ff6dad7131d9a39e690fd8a8fd982a353f1333dd4017dd4be')
    version('3.1-20160903', sha256='0ccbd2e7d46097f136fcb1aaa0d5bc24e23bb73f57d25bee5a852a683eaa7567')
    version('3.1-20150325', sha256='c88a5e4af83c5f40dda8455886ac98923a9c33125699742603a88a0253fcc8c5')

    depends_on('pkgconfig', type='build')
    depends_on('ncurses')

    def url_for_version(self, version):
        url = "http://thrysoee.dk/editline/libedit-{0}-{1}.tar.gz"
        return url.format(version[-1], version.up_to(-1))
