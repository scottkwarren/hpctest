# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RLimsolve(RPackage):
    """Solving Linear Inverse Models

    Functions that (1) find the minimum/maximum of a linear or quadratic
    function: min or max (f(x)), where f(x) = ||Ax-b||^2 or f(x) = sum(a_i*x_i)
    subject to equality constraints Ex=f and/or inequality constraints Gx>=h,
    (2) sample an underdetermined- or overdetermined system Ex=f subject to
    Gx>=h, and if applicable Ax~=b, (3) solve a linear system Ax=B for the
    unknown x. It includes banded and tridiagonal linear systems."""

    homepage = "https://cloud.r-project.org/package=limSolve"
    url      = "https://cloud.r-project.org/src/contrib/limSolve_1.5.6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/limSolve"

    version('1.5.6', sha256='b97ea9930383634c8112cdbc42f71c4e93fe0e7bfaa8f401921835cb44cb49a0')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-quadprog', type=('build', 'run'))
    depends_on('r-lpsolve', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
