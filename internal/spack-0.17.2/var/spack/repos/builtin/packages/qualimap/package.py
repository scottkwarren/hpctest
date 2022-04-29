# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Qualimap(Package):
    """Qualimap 2 is a platform-independent application written in Java
    and R that provides both a Graphical User Inteface (GUI) and a
    command-line interface to facilitate the quality control of alignment
    sequencing data and its derivatives like feature counts."""

    homepage = "http://qualimap.conesalab.org/"
    url      = "https://bitbucket.org/kokonech/qualimap/downloads/qualimap_v2.2.1.zip"

    version('2.2.1', sha256='08f1d66e49c83c76c56c4225c53aee44f41e0592c8bdc84b8c4ecd975700e045')

    depends_on('java', type='run')

    def setup_run_environment(self, env):
        env.prepend_path('PATH', prefix)

    def install(self, spec, prefix):
        install_tree('.', prefix)
