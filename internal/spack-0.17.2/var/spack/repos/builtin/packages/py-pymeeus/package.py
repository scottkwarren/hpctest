# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPymeeus(PythonPackage):
    """Library of astronomical algorithms in Python."""

    homepage = "https://github.com/architest/pymeeus"
    pypi = "PyMeeus/PyMeeus-0.3.6.tar.gz"

    version('0.3.6', sha256='1f1ba0682e1b5c6b0cd6432c966e8bc8acc31737ea6f0ae79917a2189a98bb87')

    depends_on('py-setuptools', type='build')
