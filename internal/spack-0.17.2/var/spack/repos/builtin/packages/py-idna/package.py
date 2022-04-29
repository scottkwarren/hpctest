# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class PyIdna(PythonPackage):
    """Internationalized Domain Names for Python (IDNA 2008 and UTS #46) """

    homepage = "https://github.com/kjd/idna"
    pypi = "idna/idna-3.2.tar.gz"

    version('3.2', sha256='467fbad99067910785144ce333826c71fb0e63a425657295239737f7ecd125f3')
    version('2.9', sha256='7588d1c14ae4c77d74036e8c22ff447b26d0fde8f007354fd48a7814db15b7cb')
    version('2.8', sha256='c357b3f628cf53ae2c4c05627ecc484553142ca23264e593d327bcde5e9c3407')
    version('2.5', sha256='3cb5ce08046c4e3a560fc02f138d0ac63e00f8ce5901a56b32ec8b7994082aab')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('python@3.5:',         type=('build', 'run'), when='@3.2')
    depends_on('py-setuptools', type=('build', 'link'))
