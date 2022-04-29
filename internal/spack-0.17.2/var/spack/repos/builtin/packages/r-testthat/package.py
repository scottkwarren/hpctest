# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTestthat(RPackage):
    """Unit Testing for R

    Software testing is important, but, in part because it is frustrating and
    boring, many of us avoid it. 'testthat' is a testing framework for R that
    is easy to learn and use, and integrates with your existing 'workflow'."""

    homepage = "https://github.com/hadley/testthat"
    url      = "https://cloud.r-project.org/src/contrib/testthat_1.0.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/testthat"

    version('3.0.1', sha256='297fc45c719684f11ddf9dc9088f5528fdf9b44625165543384eaf579f243ad0')
    version('2.3.2', sha256='1a268d8df07f7cd8d282d03bb96ac2d96a24a95c9aa52f4cca5138a09dd8e06c')
    version('2.2.1', sha256='67ee0512bb312695c81fd74338bb8ce9e2e58763681ddbcdfdf35f52dfdb0b78')
    version('2.1.0', sha256='cf5fa7108111b32b86e70819352f86b57ab4e835221bb1e83642d52a1fdbcdd4')
    version('1.0.2', sha256='0ef7df0ace1fddf821d329f9d9a5d42296085350ae0d94af62c45bd203c8415e')

    depends_on('r@3.1:', type=('build', 'run'))
    depends_on('r-brio', when='@3.0.1:', type=('build', 'run'))
    depends_on('r-callr@3.5.1:', when='@3.0.1:', type=('build', 'run'))
    depends_on('r-cli', when='@2.0.0:', type=('build', 'run'))
    depends_on('r-cli@2.2.0:', when='@3.0.1:', type=('build', 'run'))
    depends_on('r-crayon@1.3.4:', type=('build', 'run'))
    depends_on('r-desc', when='@3.0.1:', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-ellipsis', when='@2.3.2:', type=('build', 'run'))
    depends_on('r-ellipsis@0.2.0:', when='@3.0.1:', type=('build', 'run'))
    depends_on('r-evaluate', when='@2.2.0:', type=('build', 'run'))
    depends_on('r-jsonlite', when='@3.0.1:', type=('build', 'run'))
    depends_on('r-lifecycle', when='@3.0.1:', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-pkgload', when='@2.3.2:', type=('build', 'run'))
    depends_on('r-praise', type=('build', 'run'))
    depends_on('r-processx', when='@3.0.1:', type=('build', 'run'))
    depends_on('r-ps@1.3.4:', when='@3.0.1:', type=('build', 'run'))
    depends_on('r-r6@2.2.0:', type=('build', 'run'))
    depends_on('r-rlang@0.3.0:', when='@2.0.0:', type=('build', 'run'))
    depends_on('r-rlang@0.4.1:', when='@2.3.2:', type=('build', 'run'))
    depends_on('r-rlang@0.4.9:', when='@3.0.1:', type=('build', 'run'))
    depends_on('r-waldo@0.2.1:', when='@3.0.1:', type=('build', 'run'))
    depends_on('r-withr@2.0.0:', when='@2.0.0:', type=('build', 'run'))
    depends_on('r-withr@2.3.0:', when='@3.0.1:', type=('build', 'run'))
