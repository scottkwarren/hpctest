# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RNmof(RPackage):
    """Numerical Methods and Optimization in Finance

    Functions, examples and data from the book "Numerical Methods and
    Optimization in Finance" by M. Gilli, D. Maringer and E. Schumann (2011),
    ISBN 978-0123756626. The package provides implementations of several
    optimisation heuristics, such as Differential Evolution, Genetic Algorithms
    and Threshold Accepting. There are also functions for the valuation of
    financial instruments, such as bonds and options, and functions that help
    with stochastic simulations."""

    homepage = "http://nmof.net/"
    url      = "https://cloud.r-project.org/src/contrib/NMOF_1.6-0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/NMOF"

    version('2.2-2', sha256='e64472f89023f0d779a35df753747d750174ce89644a9142312a1d2dc6f24642')
    version('1.6-0', sha256='5484cd43c28aaf23d560c2dde8bcd8dd440a205d2214eb50e02fe0bb42ec2755')

    depends_on('r@2.14:', type=('build', 'run'))
