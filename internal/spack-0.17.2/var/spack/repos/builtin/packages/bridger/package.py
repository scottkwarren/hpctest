# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from os import symlink

from spack import *


class Bridger(MakefilePackage, SourceforgePackage):
    """Bridger : An Efficient De novo Transcriptome Assembler For
       RNA-Seq Data"""

    homepage = "https://sourceforge.net/projects/rnaseqassembly/"
    sourceforge_mirror_path = "rnaseqassembly/Bridger_r2014-12-01.tar.gz"

    version('2014-12-01', sha256='8fbec8603ea8ad2162cbd0c658e4e0a4af6453bdb53310b4b7e0d112e40b5737')

    depends_on('boost')
    depends_on('perl', type='run')

    def install(self, spec, prefix):
        # bridger depends very much on perl scripts/etc in the source tree
        install_path = join_path(prefix, 'usr/local/bridger')
        mkdirp(install_path)
        install_tree('.', install_path)

        # symlink the init script to /bin
        mkdirp(prefix.bin)
        symlink(join_path(install_path, 'Bridger.pl'),
                join_path(prefix.bin, 'Bridger.pl'))
