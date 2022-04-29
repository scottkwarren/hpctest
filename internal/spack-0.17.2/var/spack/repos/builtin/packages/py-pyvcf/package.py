# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyvcf(PythonPackage):
    """A Variant Call Format reader for Python"""

    homepage = "https://pyvcf.readthedocs.org/en/latest/index.html"
    url      = "https://github.com/jamescasbon/PyVCF/archive/v0.6.0.tar.gz"

    version('0.6.0', sha256='a360376d445e27b74db3216f6931a94a4ea99aa4a7f4b4a8347e7f11836698b9')

    depends_on('py-setuptools', type='build')
