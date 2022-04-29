# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Webbench(MakefilePackage):
    """Webbench is a simple website pressure test tool used in Linux."""

    homepage = "http://home.tiscali.cz/~cz210552/webbench.html"
    git      = "https://github.com/EZLippi/WebBench.git"

    version('1.5', commit='b1acf3c01cc914729fe188dfc8ed761858028d4f')

    depends_on('ntirpc')

    def setup_build_environment(self, env):
        env.prepend_path('CPATH', self.spec['ntirpc'].prefix.include.ntirpc)

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')
        makefile.filter('$(DESTDIR)/usr/local/man/man1', self.prefix.man.man1,
                        string=True)

    def install(self, spec, prefix):
        make('install', 'PREFIX={0}'.format(prefix))
