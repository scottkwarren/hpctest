# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFypp(PythonPackage):
    """Python powered Fortran preprocessor."""

    homepage = "https://github.com/aradi/fypp"
    url      = "https://github.com/aradi/fypp/archive/2.1.1.zip"

    version('2.1.1', sha256='3744ad17045e91466bbb75a33ce0cab0f65bc2c377127067a932cdf15655e049')

    depends_on('py-setuptools', type='build')
