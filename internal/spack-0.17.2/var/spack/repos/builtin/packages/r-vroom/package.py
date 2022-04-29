# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RVroom(RPackage):
    """Read and Write Rectangular Text Data Quickly.

    The goal of 'vroom' is to read and write data (like 'csv', 'tsv' and
    'fwf') quickly. When reading it uses a quick initial indexing step, then
    reads the values lazily , so only the data you actually use needs to be
    read. The writer formats the data in parallel and writes to disk
    asynchronously from formatting."""

    homepage = "https://github.com/r-lib/vroom"
    cran     = "vroom"

    version('1.5.5', sha256='1d45688c08f162a3300eda532d9e87d144f4bc686769a521bf9a12e3d3b465fe')

    depends_on('r@3.1:', type=('build', 'run'))
    depends_on('r-bit64', type=('build', 'run'))
    depends_on('r-crayon', type=('build', 'run'))
    depends_on('r-cli', type=('build', 'run'))
    depends_on('r-glue', type=('build', 'run'))
    depends_on('r-hms', type=('build', 'run'))
    depends_on('r-lifecycle', type=('build', 'run'))
    depends_on('r-rlang@0.4.2:', type=('build', 'run'))
    depends_on('r-tibble@2.0.0:', type=('build', 'run'))
    depends_on('r-tzdb@0.1.1:', type=('build', 'run'))
    depends_on('r-vctrs@0.2.0:', type=('build', 'run'))
    depends_on('r-tidyselect', type=('build', 'run'))
    depends_on('r-withr', type=('build', 'run'))
    depends_on('r-progress@1.2.1:', type=('build', 'run'))
    depends_on('r-cpp11@0.2.0:', type=('build', 'run'))
