# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDoxypypy(PythonPackage):
    """A Doxygen filter for Python.

    A more Pythonic version of doxypy, a Doxygen filter for Python.
    """

    homepage = "https://github.com/Feneric/doxypypy"
    pypi = "doxypypy/doxypypy-0.8.8.6.tar.gz"

    version('0.8.8.6', sha256='627571455c537eb91d6998d95b32efc3c53562b2dbadafcb17e49593e0dae01b')

    depends_on('py-setuptools', type='build')
