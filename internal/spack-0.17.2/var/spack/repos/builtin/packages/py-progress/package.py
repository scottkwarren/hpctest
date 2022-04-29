# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyProgress(PythonPackage):
    """Easy progress reporting for Python"""

    homepage = "https://github.com/verigak/progress/"
    pypi = "progress/progress-1.4.tar.gz"

    version('1.4', sha256='5e2f9da88ed8236a76fffbee3ceefd259589cf42dfbc2cec2877102189fae58a')

    depends_on('py-setuptools', type='build')
