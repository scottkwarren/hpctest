# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCppheaderparser(PythonPackage):
    """Parse C++ header files and generate a data structure
    representing the class"""

    pypi = "CppHeaderParser/CppHeaderParser-2.7.4.tar.gz"

    version('2.7.4', sha256='382b30416d95b0a5e8502b214810dcac2a56432917e2651447d3abe253e3cc42')

    depends_on('py-setuptools', type='build')
    depends_on('py-ply', type=('build', 'run'))
