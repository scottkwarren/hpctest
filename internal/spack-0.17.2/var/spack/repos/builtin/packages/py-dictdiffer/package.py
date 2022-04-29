# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDictdiffer(PythonPackage):
    """Dictdiffer is a helper module that helps you to diff and patch dictionares."""

    homepage = "https://github.com/inveniosoftware/dictdiffer"
    pypi     = "dictdiffer/dictdiffer-0.8.1.tar.gz"

    version('0.8.1', sha256='1adec0d67cdf6166bda96ae2934ddb5e54433998ceab63c984574d187cc563d2')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-setuptools-scm@3.1.0:', type='build')
    depends_on('py-pytest-runner@2.7:', type='build')
