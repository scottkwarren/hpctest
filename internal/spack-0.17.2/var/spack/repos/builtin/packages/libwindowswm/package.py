# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libwindowswm(AutotoolsPackage, XorgPackage):
    """WindowsWM - Cygwin/X rootless window management extension.

    WindowsWM is a simple library designed to interface with the
    Windows-WM extension.  This extension allows X window managers to
    better interact with the Cygwin XWin server when running X11 in a
    rootless mode."""

    homepage = "https://cgit.freedesktop.org/xorg/lib/libWindowsWM"
    xorg_mirror_path = "lib/libWindowsWM-1.0.1.tar.gz"

    version('1.0.1', sha256='94f9c0add3bad38ebd84bc43d854207c4deaaa74fb15339276e022546124b98a')

    depends_on('libx11')
    depends_on('libxext')

    depends_on('xextproto')
    depends_on('windowswmproto')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
