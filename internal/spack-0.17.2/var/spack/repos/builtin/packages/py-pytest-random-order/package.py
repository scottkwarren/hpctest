# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyPytestRandomOrder(PythonPackage):
    """
    Randomise the order in which pytest tests are run.
    """

    homepage = "https://github.com/jbasko/pytest-random-order"
    pypi     = "pytest-random-order/pytest-random-order-1.0.4.tar.gz"

    version('1.0.4', sha256='6b2159342a4c8c10855bc4fc6d65ee890fc614cb2b4ff688979b008a82a0ff52')

    depends_on('python@3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-pytest@3.0.0:', type=('build', 'test', 'run'))
    depends_on('py-coverage', type=('test', 'run'))
    depends_on('py-pytest-xdist', type=('test', 'run'))
    depends_on('py-sphinx', type=('test', 'run'))
    depends_on('py-tox', type=('test', 'run'))
    depends_on('py-py', type=('test', 'run'))
