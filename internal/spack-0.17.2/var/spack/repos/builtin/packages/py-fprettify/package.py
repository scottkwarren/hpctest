# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFprettify(PythonPackage):
    """fprettify is an auto-formatter for modern Fortran code (Fortran 90
    and later) that imposes strict whitespace formatting, written in
    Python."""

    homepage = "https://github.com/pseewald/fprettify"
    pypi = "fprettify/fprettify-0.3.6.tar.gz"

    version('0.3.6', sha256='5ee954763eba2bc54ee7444c1f592944f1c1933223bb0c07957d60d44f7f0b75')

    depends_on('py-setuptools', type='build')
    depends_on('py-configargparse', type=('build', 'run'))
