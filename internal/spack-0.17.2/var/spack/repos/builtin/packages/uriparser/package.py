# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Uriparser(CMakePackage):
    """uriparser is a strictly RFC 3986 compliant URI parsing and handling
    library written in C89 ("ANSI C")."""

    homepage = "https://uriparser.github.io/"
    url      = "https://github.com/uriparser/uriparser/releases/download/uriparser-0.9.3/uriparser-0.9.3.tar.gz"

    version('0.9.5', sha256='1987466a798becb5441a491d29e762ab1a4817a525f82ef239e3d38f85605a77')
    version('0.9.3', sha256='6cef39d6eaf1a48504ee0264ce85f078758057dafb1edd0a898183b55ff76014')

    variant('docs', default=False, description='Build API documentation')

    depends_on('cmake@3.3:', type='build')
    depends_on('googletest@1.8.1', type='link')
    depends_on('doxygen', when='+docs', type='build')
    depends_on('graphviz', when='+docs', type='build')

    def cmake_args(self):
        args = []

        if self.run_tests:
            args.append('-DURIPARSER_BUILD_TESTS:BOOL=ON')
        else:
            args.append('-DURIPARSER_BUILD_TESTS:BOOL=OFF')

        if '+docs' in self.spec:
            args.append('-DURIPARSER_BUILD_DOCS:BOOL=ON')
        else:
            args.append('-DURIPARSER_BUILD_DOCS:BOOL=OFF')

        return args
