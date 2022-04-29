# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xclipboard(AutotoolsPackage, XorgPackage):
    """xclipboard is used to collect and display text selections that are
    sent to the CLIPBOARD by other clients.  It is typically used to save
    CLIPBOARD selections for later use.  It stores each CLIPBOARD
    selection as a separate string, each of which can be selected."""

    homepage = "https://cgit.freedesktop.org/xorg/app/xclipboard"
    xorg_mirror_path = "app/xclipboard-1.1.3.tar.gz"

    version('1.1.3', sha256='a8c335cf166cbb27ff86569503db7e639f85741ad199bfb3ba45dd0cfda3da7f')

    depends_on('libxaw')
    depends_on('libxmu')
    depends_on('libxt@1.1:')
    depends_on('libx11')
    depends_on('libxkbfile')

    depends_on('xproto@7.0.17:')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
