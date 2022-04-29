# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyStestr(PythonPackage):
    """A parallel Python test runner built around subunit."""

    homepage = "https://stestr.readthedocs.io/en/latest/"
    pypi = "stestr/stestr-2.5.1.tar.gz"

    version('2.5.1', sha256='151479fdf2db9f5f492b5285f4696f2d38960639054835dbdcd4c0687122c0fd')

    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
