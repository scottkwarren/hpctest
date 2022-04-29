# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libbacktrace(AutotoolsPackage):
    """A C library that may be linked into a C/C++ program to produce
    symbolic backtraces."""

    homepage = "https://github.com/ianlancetaylor/libbacktrace"
    git      = "https://github.com/ianlancetaylor/libbacktrace.git"
    maintainers = ['trahay']

    version('master',  branch='master')
    version('2020-02-19', commit='ca0de0517f3be44fedf5a2c01cfaf6437d4cae68')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
