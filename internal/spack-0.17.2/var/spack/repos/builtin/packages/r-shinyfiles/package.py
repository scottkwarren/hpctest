# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RShinyfiles(RPackage):
    """A Server-Side File System Viewer for Shiny

    Provides functionality for client-side navigation of the server side
    file system in shiny apps. In case the app is running locally this gives
    the user direct access to the file system without the need to "download"
    files to a temporary location. Both file and folder selection as well as
    file saving is available."""

    homepage = "https://github.com/thomasp85/shinyFiles"
    url      = "https://cloud.r-project.org/src/contrib/shinyFiles_0.7.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/shinyFiles"

    version('0.9.0', sha256='51ad2aad61bcae22fb2c48a79d02bf6f86e36ffc49a3b64e26a76d133a955167')
    version('0.7.3', sha256='710c8a6191aaf336379bc748daff1160d0d2858e2aee0d98e2ad48e7121d5a05')

    depends_on('r-htmltools', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-shiny@1.1.0:', type=('build', 'run'))
    depends_on('r-fs@1.2.6:', type=('build', 'run'))
    depends_on('r-tibble@1.4.2:', type=('build', 'run'))
