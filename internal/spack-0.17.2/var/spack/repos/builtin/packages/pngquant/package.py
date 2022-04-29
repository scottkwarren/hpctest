# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pngquant(AutotoolsPackage):
    """
    pngquant is a command-line utility and a library for lossy compression of
    PNG images.
    """

    homepage = "https://pngquant.org/"
    url      = "https://pngquant.org/pngquant-2.12.5-src.tar.gz"

    version('2.12.5', sha256='3638936cf6270eeeaabcee42e10768d78e4dc07cac9310307835c1f58b140808')

    depends_on('libpng')
