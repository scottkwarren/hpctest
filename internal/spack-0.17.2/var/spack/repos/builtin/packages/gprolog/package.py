# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gprolog(Package):
    """A free Prolog compiler with constraint solving over finite domains."""
    homepage = "http://www.gprolog.org/"
    url      = "http://www.gprolog.org/gprolog-1.4.5.tar.gz"

    version('1.4.5', sha256='bfdcf00e051e0628b4f9af9d6638d4fde6ad793401e58a5619d1cc6105618c7c')

    parallel = False

    def install(self, spec, prefix):
        with working_dir('src'):
            configure('--with-install-dir=%s' % prefix,
                      '--without-links-dir')
            make()
            make('install')
