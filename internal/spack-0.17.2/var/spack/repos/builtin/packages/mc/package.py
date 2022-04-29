# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mc(AutotoolsPackage):
    """The GNU Midnight Commander is a visual file manager."""

    homepage = "https://midnight-commander.org"
    url      = "http://ftp.midnight-commander.org/mc-4.8.20.tar.bz2"

    version('4.8.26', sha256='9d6358d0a351a455a1410aab57f33b6b48b0fcf31344b9a10b0ff497595979d1')
    version('4.8.23', sha256='238c4552545dcf3065359bd50753abbb150c1b22ec5a36eaa02c82808293267d')
    version('4.8.21', sha256='251d9f0ef9309ef3eea0fdc4c12b8b61149e5056bef1b2de2ccc7f015d973444')
    version('4.8.20', sha256='2d85daaa6ab26e524946df4823ac2f69802bc16bc967781b5e28d5b86fc3b979')

    depends_on('ncurses')
    depends_on('pkgconfig', type='build')
    depends_on('glib@2.14:')
    depends_on('libssh2@1.2.5:')

    def setup_build_environment(self, env):
        # Fix compilation bug on macOS by pretending we don't have utimensat()
        # https://github.com/MidnightCommander/mc/pull/130
        if 'darwin' in self.spec.architecture:
            env.set('ac_cv_func_utimensat', 'no')

    def configure_args(self):
        args = [
            '--disable-debug',
            '--disable-dependency-tracking',
            '--disable-silent-rules',
            '--without-x',
            '--with-screen=ncurses',
            '--enable-vfs-sftp'
        ]
        return args
