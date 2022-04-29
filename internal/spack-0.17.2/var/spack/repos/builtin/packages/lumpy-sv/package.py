# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class LumpySv(MakefilePackage):
    """A probabilistic framework for structural variant discovery."""

    homepage = "https://github.com/arq5x/lumpy-sv"
    url      = "https://github.com/arq5x/lumpy-sv/archive/0.2.13.tar.gz"

    version('0.2.13', sha256='3672b86ef0190ebe520648a6140077ee9f15b0549cb233dca18036e63bbf6375')

    depends_on('htslib')

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')
        makefile.filter('export CXX .*', '')

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
