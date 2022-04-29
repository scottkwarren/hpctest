# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGlobals(RPackage):
    """Identify Global Objects in R Expressions

    Identifies global ("unknown" or "free") objects in R expressions by code
    inspection using various strategies, e.g. conservative or liberal. The
    objective of this package is to make it as simple as possible to identify
    global objects for the purpose of exporting them in distributed compute
    environments."""

    homepage = "https://github.com/HenrikBengtsson/globals"
    url      = "https://cloud.r-project.org/src/contrib/globals_0.12.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/globals"

    version('0.14.0', sha256='203dbccb829ca9cc6aedb6f5e79cb126ea31f8dd379dff9111ec66e3628c32f3')
    version('0.12.4', sha256='7985356ad75afa1f795f8267a20dee847020c0207252dc075c614cef55d8fe6b')

    depends_on('r@3.1.2:', type=('build', 'run'))
    depends_on('r-codetools', type=('build', 'run'))
