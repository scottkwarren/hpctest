# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyPytestDoctestplus(PythonPackage):
    """Pytest plugin with advanced doctest features."""

    homepage = "https://www.astropy.org/"
    pypi     = "pytest-doctestplus/pytest-doctestplus-0.8.0.tar.gz"

    version('0.9.0', sha256='6fe747418461d7b202824a3486ba8f4fa17a9bd0b1eddc743ba1d6d87f03391a')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools@30.3.0:', type=('build', 'run'))
    depends_on('py-setuptools-scm', type='build')
    depends_on('py-pytest@4.6:', type=('build', 'run'))
