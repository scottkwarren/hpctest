# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class GosamContrib(AutotoolsPackage):
    """Additional libraries for GoSam MC generator"""

    homepage = "https://gosam.hepforge.org"
    url      = "https://gosam.hepforge.org/downloads/?f=gosam-contrib-2.0.tar.gz"

    tags = ['hep']

    version('2.0', sha256='c05beceea74324eb51c1049773095e2cb0c09c8c909093ee913d8b0da659048d')
    version('1.0', sha256='a29d4232d9190710246abc2ed97fdcd8790ce83580f56a360f3456b0377c40ec')

    variant('libs', default='shared,static', values=('shared', 'static'),
            multi=True, description='Build shared libs, static libs or both')
    variant('pic', default=False, description='Build position-independent code')

    def flag_handler(self, name, flags):
        if name in ['cflags', 'cxxflags', 'cppflags']:
            if '+pic' in self.spec:
                flags.append(self.compiler.cc_pic_flag)

        if name == 'fflags':
            if 'gfortran' in self.compiler.fc:
                flags.append('-std=legacy')

            if '+pic' in self.spec:
                flags.append(self.compiler.fc_pic_flag)

        return (None, flags, None)

    def configure_args(self):
        args = []
        args += self.enable_or_disable('libs')

        return args

    @property
    def parallel(self):
        return False
