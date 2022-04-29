# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Acct(AutotoolsPackage):
    """Utilities for monitoring process activities."""

    homepage = "https://www.gnu.org/software/acct"
    url      = "https://ftp.gnu.org/gnu/acct/acct-6.6.4.tar.gz"

    version('6.6.4', sha256='4c15bf2b58b16378bcc83f70e77d4d40ab0b194acf2ebeefdb507f151faa663f')
    version('6.6.3', sha256='5eae79323bf1ce403704d2b70483c46e7c853276ee7b5ad561ec3ccae9fca093')
    version('6.6.2', sha256='8ed47b2f893b08f0d67720880adbb48b835a826c314fa52fd52af1cee6870101')

    def setup_run_environment(self, env):
        env.prepend_path('PATH', self.prefix.sbin)

    def installcheck(self):
        """"Runs standard check if all programs support --help but not all do"""
        pass
