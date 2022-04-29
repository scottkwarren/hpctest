# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyWhichcraft(PythonPackage):
    """Cross-platform cross-python shutil.which functionality."""

    homepage = "https://github.com/pydanny/whichcraft"
    url      = "https://github.com/pydanny/whichcraft/archive/0.4.1.tar.gz"

    version('0.4.1', sha256='66875022b3b9da8ddf7ab236c15670a782094550d07daeb51ceba4bc61b6b4aa')

    depends_on('py-setuptools', type='build')
