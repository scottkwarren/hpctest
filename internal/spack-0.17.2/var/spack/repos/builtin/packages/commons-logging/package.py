# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class CommonsLogging(Package):
    """When writing a library it is very useful to log information. However
    there are many logging implementations out there, and a library cannot
    impose the use of a particular one on the overall application that the
    library is a part of.

    The Logging package is an ultra-thin bridge between different logging
    implementations. A library that uses the commons-logging API can be used
    with any logging implementation at runtime. Commons-logging comes with
    support for a number of popular logging implementations, and writing
    adapters for others is a reasonably simple task."""

    homepage = "https://commons.apache.org/proper/commons-logging/"
    url      = "https://archive.apache.org/dist/commons/logging/binaries/commons-logging-1.2-bin.tar.gz"

    version('1.2',   sha256='3f758805c7290d9c6d22d1451587c9f7232744aef4c984e88aa683cdea0587bd')
    version('1.1.3', sha256='9e7093c93529792563b5c19ab5cccb73ef4ca7d82b886bdec6d0af182ba9908a')
    version('1.1.1', sha256='88c721d66f570a87f710a2449f0e3bffea86489d9dd2fa70b805104c4f8d69e6')

    extends('jdk')
    depends_on('java', type='run')

    def install(self, spec, prefix):
        install('commons-logging-{0}.jar'.format(self.version), prefix)
