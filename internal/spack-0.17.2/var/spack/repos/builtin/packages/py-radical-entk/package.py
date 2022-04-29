# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRadicalEntk(PythonPackage):
    """RADICAL Ensemble Toolkit is used for developing and executing
    large-scale ensemble-based workflows."""

    homepage = 'https://radical-cybertools.github.io'
    git      = 'https://github.com/radical-cybertools/radical.entk.git'
    pypi     = 'radical.entk/radical.entk-1.8.0.tar.gz'

    maintainers = ['andre-merzky']

    version('develop', branch='devel')
    version('1.8.0',   sha256='47a3f7f1409612d015a3e6633853d31ec4e4b0681aecb7554be16ebf39c7f756')
    version('1.6.7',   sha256='9384568279d29b9619a565c075f287a08bca8365e2af55e520af0c2f3595f8a2')

    depends_on('py-radical-utils', type=('build', 'run'))
    depends_on('py-radical-pilot', type=('build', 'run'))

    depends_on('python@3.6:',      type=('build', 'run'))
    depends_on('py-pika@0.13.0',   type=('build', 'run'))
    depends_on('py-setuptools',    type='build')
