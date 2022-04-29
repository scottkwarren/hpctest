# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLazy(PythonPackage):
    """Lazy attributes for Python objects"""

    pypi = "lazy/lazy-1.2.zip"

    version('1.2', sha256='127ea610418057b953f0d102bed83f2c367be13b59f8d0ddf3b8a86c7d31b970')

    depends_on('py-setuptools', type='build')
