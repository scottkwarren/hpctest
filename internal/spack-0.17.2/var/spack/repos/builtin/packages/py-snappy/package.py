# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySnappy(PythonPackage):
    """A pure python implementation of the Snappy compression algorithm."""

    homepage = "https://github.com/ethereum/py-snappy"
    url      = "https://github.com/ethereum/py-snappy/archive/v0.1.0-alpha.1.tar.gz"

    version('0.1.0-alpha.1', sha256='f94c5bfc0b2bb42f7d442f0d84c9ffd9aa92876632d415612f25bafa61ddcfc4')

    patch('req.patch')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
