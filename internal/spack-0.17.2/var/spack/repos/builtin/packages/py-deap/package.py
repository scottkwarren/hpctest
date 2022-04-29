# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDeap(PythonPackage):
    """Distributed Evolutionary Algorithms in Python."""

    homepage = "https://deap.readthedocs.org/"
    pypi = "deap/deap-1.3.1.tar.gz"

    version('1.3.1', sha256='11f54493ceb54aae10dde676577ef59fc52d52f82729d5a12c90b0813c857a2f')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
