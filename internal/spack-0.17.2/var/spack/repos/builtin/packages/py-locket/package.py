# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLocket(PythonPackage):
    """File-based locks for Python for Linux and Windows."""

    homepage = "https://github.com/mwilliamson/locket.py"
    pypi = "locket/locket-0.2.0.tar.gz"

    version('0.2.0', sha256='1fee63c1153db602b50154684f5725564e63a0f6d09366a1cb13dffcec179fb4')
