# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGmp(RPackage):
    """Multiple Precision Arithmetic

    Multiple Precision Arithmetic (big integers and rationals, prime number
    tests, matrix computation), "arithmetic without limitations" using the C
    library GMP (GNU Multiple Precision Arithmetic)."""

    homepage = "http://mulcyber.toulouse.inra.fr/projects/gmp"
    url      = "https://cloud.r-project.org/src/contrib/gmp_0.5-13.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/gmp"

    version('0.6-2', sha256='6bfcb45b3f1e7da27d8773f911027355cab371d150c3dabf7dbaf8fba85b7f0e')
    version('0.5-13.5', sha256='f681ab2ff3d1e379ba8ac44a8abddd08d08170723e885abc0b469b6fa8fe5510')
    version('0.5-13.4', sha256='f05605b40fc39fc589e3a4d2f526a591a649faa45eef7f95c096e1bff8775196')
    version('0.5-13.1', sha256='2f805374a26742cd43f6b2054130d8670eda1940070aabb9971e9e48226d0976')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r@3.5.0:', when='@0.6-2:', type=('build', 'run'))
    depends_on('gmp@4.2.3:')
