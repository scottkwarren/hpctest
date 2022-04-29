# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class NosourceInstall(BundlePackage):
    """Simple bundle package with one dependency and metadata 'install'."""

    homepage = "http://www.example.com"

    version('2.0')
    version('1.0')

    depends_on('dependency-install')

    # The install phase must be specified.
    phases = ['install']

    # The install method must also be present.
    def install(self, spec, prefix):
        touch(join_path(self.prefix, 'install.txt'))

    @run_after('install')
    def post_install(self):
        touch(join_path(self.prefix, 'post-install.txt'))
