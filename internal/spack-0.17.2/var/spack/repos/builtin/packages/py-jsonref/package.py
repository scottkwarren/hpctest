# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJsonref(PythonPackage):
    """An implementation of JSON Reference for Python"""

    homepage = "https://github.com/gazpachoking/jsonref"
    pypi = "jsonref/jsonref-0.2.tar.gz"

    version('0.2', sha256='f3c45b121cf6257eafabdc3a8008763aed1cd7da06dbabc59a9e4d2a5e4e6697')

    depends_on('py-setuptools', type='build')
