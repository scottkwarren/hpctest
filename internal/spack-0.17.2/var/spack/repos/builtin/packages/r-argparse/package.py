# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RArgparse(RPackage):
    """Command Line Optional and Positional Argument Parser

    A command line parser to be used with Rscript to write "#!" shebang scripts
    that gracefully accept positional and optional arguments and automatically
    generate usage."""

    homepage = "https://github.com/trevorld/argparse"
    url      = "https://cloud.r-project.org/src/contrib/argparse_1.1.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/argparse"

    version('2.0.3', sha256='d26139c610ea0adf8d6632699cd34c4595ae3e7963bfc7a00cb3b7504f2059b0')
    version('2.0.1', sha256='949843920d14fc7c162aedab331a936499541736e7dafbb103fbfd79be8147ab')
    version('1.1.1', sha256='441449f0816411a868fd1b15cf4b2bc45931bbd4b67d6592dbe48875905cf93b')

    depends_on('r-proto@1:', when='@1.0.0:1.9.9', type=('build', 'run'))
    depends_on('r-getopt', when='@1.0.0:1.9.9', type=('build', 'run'))
    depends_on('r-r6', when='@2.0.0:', type=('build', 'run'))
    depends_on('r-findpython', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('python@3.2:', type=('build', 'run'))
