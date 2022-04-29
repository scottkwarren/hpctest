# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTermcolor(PythonPackage):
    """ANSII Color formatting for output in terminal."""

    pypi = "termcolor/termcolor-1.1.0.tar.gz"

    version('1.1.0', sha256='1d6d69ce66211143803fbc56652b41d73b4a400a2891d7bf7a1cdf4c02de613b')
