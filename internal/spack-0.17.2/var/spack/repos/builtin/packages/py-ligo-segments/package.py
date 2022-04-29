# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLigoSegments(PythonPackage):
    """Representations of semi-open intervals."""

    pypi = "ligo-segments/ligo-segments-1.2.0.tar.gz"

    version('1.2.0', sha256='5edbcb88cae007c4e154a61cb2c9d0a6d6d4016c1ecaf0a59a667a267bd20e7a')

    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))
