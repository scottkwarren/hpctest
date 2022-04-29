# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTensor(RPackage):
    """The tensor product of two arrays is notionally an outer product of
       the arrays collapsed in specific extents by summing along the
       appropriate diagonals.
    """

    homepage = "https://cloud.r-project.org/package=tensor"
    url      = "https://cloud.r-project.org/src/contrib/tensor_1.5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/tensor"

    version('1.5', sha256='e1dec23e3913a82e2c79e76313911db9050fb82711a0da227f94fc6df2d3aea6')
    version('1.4', sha256='6f1643da018d58a0aaa27260df6fdf687fc36f4cd1964931b3180b7df8c0e642')
