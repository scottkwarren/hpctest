# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Elsd(MakefilePackage):
    """ELSD: Ellipse and Line Segment Detector"""

    homepage = "http://ubee.enseeiht.fr/vision/ELSD/"
    git      = "https://github.com/viorik/ELSD.git"

    version('master', branch='master')

    depends_on('blas')
    depends_on('lapack')

    def edit(self, spec, prefix):
        lapack_blas = spec['lapack'].libs + spec['blas'].libs

        makefile = FileFilter('makefile')
        makefile.filter('-llapack -lblas', lapack_blas.link_flags)

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('elsd', prefix.bin)
