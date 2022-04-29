# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPytestIsort(PythonPackage):
    """py.test plugin to check import ordering using isort"""

    homepage = "https://github.com/moccu/pytest-isort/"
    pypi = "pytest-isort/pytest-isort-0.3.1.tar.gz"

    version('0.3.1', sha256='4bfee60dad1870b51700d55a85f5ceda766bd9d3d2878c1bbabee80e61b1be1a')

    depends_on('py-pytest@3.5:', type=('build', 'run'))
    depends_on('py-isort@4.0:', type=('build', 'run'))
