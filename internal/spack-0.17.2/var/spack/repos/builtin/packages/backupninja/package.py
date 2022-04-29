# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Backupninja(AutotoolsPackage):
    """Backupninja backup tool."""

    homepage = "https://github.com/lelutin/backupninja"
    git      = "https://github.com/lelutin/backupninja.git"

    version('master', branch='master')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('bash',     type='build')
    depends_on('gawk',     type='build')

    def setup_run_environment(self, env):
        env.prepend_path('PATH', self.prefix.sbin)
