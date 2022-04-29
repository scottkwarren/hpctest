# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PsLite(CMakePackage):
    """ps-lite is A light and efficient implementation
    of the parameter server framework."""

    homepage = "https://github.com/dmlc/ps-lite"
    git      = "https://github.com/dmlc/ps-lite.git"

    version('master', branch='master')
    version('20170328', commit='acdb698fa3bb80929ef83bb37c705f025e119b82')

    depends_on('protobuf@3:')
    depends_on('libzmq')

    patch('cmake.patch')
