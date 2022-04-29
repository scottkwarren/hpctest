# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
class V1Provider(Package):
    """Mimic the real netlib-lapack, that may be built on top of an
    optimized blas.
    """
    homepage = "https://dev.null"

    version('1.0')

    provides('v1')
