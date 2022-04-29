# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPymysql(PythonPackage):
    """Pure-Python MySQL client library"""

    homepage = "https://github.com/PyMySQL/PyMySQL/"
    pypi = "pymysql/PyMySQL-0.9.2.tar.gz"

    version('0.9.2', sha256='9ec760cbb251c158c19d6c88c17ca00a8632bac713890e465b2be01fdc30713f')

    depends_on('py-setuptools', type='build')
    depends_on('py-cryptography', type=('build', 'run'))
