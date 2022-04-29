# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sailfish(CMakePackage):
    """Sailfish is a tool for transcript quantification from RNA-seq data."""

    homepage = "https://www.cs.cmu.edu/~ckingsf/software/sailfish"
    url      = "https://github.com/kingsfordgroup/sailfish/archive/v0.10.1.tar.gz"

    version('0.10.1', sha256='a0d6d944382f2e07ffbfd0371132588e2f22bb846ecfc3d3435ff3d81b30d6c6')

    depends_on('boost@1.55:')
    depends_on('tbb')
