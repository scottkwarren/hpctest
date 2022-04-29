# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Freeglut(CMakePackage, SourceforgePackage):
    """FreeGLUT is a free-software/open-source alternative to the OpenGL
       Utility Toolkit (GLUT) library"""

    homepage = "http://freeglut.sourceforge.net/"
    sourceforge_mirror_path = "freeglut/freeglut-3.2.1.tar.gz"

    version('3.2.1', sha256='d4000e02102acaf259998c870e25214739d1f16f67f99cb35e4f46841399da68')
    version('3.0.0', sha256='2a43be8515b01ea82bcfa17d29ae0d40bd128342f0930cd1f375f1ff999f76a2')

    depends_on('pkgconfig', type='build')
    depends_on('gl')
    depends_on('glu')
    depends_on('libx11')
    depends_on('libxrandr')
    depends_on('libxi')
    depends_on('libxxf86vm')
    depends_on('xrandr')
    depends_on('inputproto')

    # freeglut fails to build with -fno-common (default with newer compilers)
    # see https://bugs.gentoo.org/705840 and https://github.com/dcnieho/FreeGLUT/pull/76
    patch('https://gitweb.gentoo.org/repo/gentoo.git/plain/media-libs/freeglut/files/freeglut-3.2.1-gcc10-fno-common.patch?id=f9102571b69d9fc05471a592fda252681fdfdef1',
          sha256='898e8fb314cbe728d791e9ea69829313143cda039c008f0ca06c1b5730922aa7',
          when="@3.2.1: %gcc@10.0:")
    patch('https://gitweb.gentoo.org/repo/gentoo.git/plain/media-libs/freeglut/files/freeglut-3.2.1-gcc10-fno-common.patch?id=f9102571b69d9fc05471a592fda252681fdfdef1',
          sha256='898e8fb314cbe728d791e9ea69829313143cda039c008f0ca06c1b5730922aa7',
          when="@3.2.1: %clang@11.0:")

    def cmake_args(self):
        return [
            '-DFREEGLUT_BUILD_DEMOS=OFF',
            '-DOPENGL_gl_LIBRARY=' + self.spec['gl'].libs[0],
            '-DOPENGL_glu_LIBRARY=' + self.spec['glu'].libs[0],
            '-DX11_X11_LIB=' + self.spec['libx11'].libs[0],
            '-DX11_Xrandr_LIB=' + self.spec['libxrandr'].libs[0],
            '-DX11_Xi_LIB=' + self.spec['libxi'].libs[0],
            '-DX11_Xxf86vm_LIB=' + self.spec['libxxf86vm'].libs[0],
        ]
