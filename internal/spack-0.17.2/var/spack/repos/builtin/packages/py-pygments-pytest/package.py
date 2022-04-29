# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPygmentsPytest(PythonPackage):
    """A pygments lexer for pytest output."""

    homepage = "https://github.com/asottile/pygments-pytest"
    pypi = "pygments-pytest/pygments_pytest-1.2.0.tar.gz"

    version('1.2.0', sha256='fc48e2fffd6d3c047a61c1db8b88ab069983f50e733fe70a7846098eb28bc955')

    depends_on('py-setuptools', type='build')
