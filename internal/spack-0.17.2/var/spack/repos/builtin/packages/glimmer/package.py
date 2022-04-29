# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Glimmer(MakefilePackage):
    """Glimmer is a system for finding genes in microbial DNA, especially the
    genomes of bacteria, archaea, and viruses."""

    homepage = "https://ccb.jhu.edu/software/glimmer"

    version('3.02b', sha256='ecf28e03d0a675aed7360ca34ca7f19993f5c3ea889273e657ced9fa7d1e2bf6')

    build_directory = 'src'

    def url_for_version(self, version):
        url = "https://ccb.jhu.edu/software/glimmer/glimmer{0}.tar.gz"
        return url.format(version.joined)

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
