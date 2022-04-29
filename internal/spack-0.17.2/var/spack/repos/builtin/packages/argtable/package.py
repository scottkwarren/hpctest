# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Argtable(AutotoolsPackage):
    """Argtable is an ANSI C library for parsing GNU style command line
       options with a minimum of fuss.
    """

    homepage = "http://argtable.sourceforge.net/"
    url      = "https://sourceforge.net/projects/argtable/files/argtable/argtable-2.13/argtable2-13.tar.gz/download"

    version('2-13', sha256='8f77e8a7ced5301af6e22f47302fdbc3b1ff41f2b83c43c77ae5ca041771ddbf')
