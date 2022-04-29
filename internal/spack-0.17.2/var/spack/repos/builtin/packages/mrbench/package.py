# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Mrbench(MavenPackage):
    """A simple Java tool for SMTP server benchmarking."""

    homepage = "https://github.com/marcorosi/mrbench"
    git      = "https://github.com/marcorosi/mrbench.git"

    version('master', branch='master')

    depends_on('java@8', type=('build', 'run'))
