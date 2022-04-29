# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyepsg(PythonPackage):
    """Provides simple access to https://epsg.io/."""

    homepage = "https://pyepsg.readthedocs.io/en/latest/"
    pypi = "pyepsg/pyepsg-0.3.2.tar.gz"

    version('0.3.2', sha256='597ef8c0e8c1be3db8f68c5985bcfbbc32e22f087e93e81ceb03ff094898e059')

    depends_on('py-setuptools', type='build')
    depends_on('py-requests',   type=('build', 'run'))
