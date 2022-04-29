# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Asciidoc(AutotoolsPackage):
    """A presentable text document format for writing articles, UNIX man
    pages and other small to medium sized documents."""

    homepage = "https://asciidoc.org/"
    # Always working URL but strangely with another checksum
    url      = "https://github.com/asciidoc-py/asciidoc-py/archive/8.6.10.tar.gz"
    git      = "https://github.com/asciidoc-py/asciidoc-py.git"

    version('master', branch='master')
    version('9.1.0',  sha256='5056c20157349f8dc74f005b6e88ccbf1078c4e26068876f13ca3d1d7d045fe7')
    version('9.0.5',  sha256='edc8328c3682a8568172656f6fc309b189f65219a49517966c7ea144cb25f8b2')
    version('9.0.4',  sha256='fb0e683ae6a4baf34a8969c3af764ca729526196576729ee9275b9f39fd8b79c')
    version('9.0.3',  sha256='b6ef4accd7959f51b532ab4d3aaa211e15f18fd544c4c3cc3ed712f5590a50de')
    version('9.0.2',  sha256='93fbe32d56380afee2f26389d8ebfdf33de72536449d53308120d3c20d2c1e17')
    version('8.6.10', sha256='22d6793d4f48cefb4a6963853212a214591a591ece1bcbc56af3c67c642003ea')
    version('8.6.9',  sha256='45e95bed1e341980f7de0a66fdc467090956fe55d4625bdad8057cd926e0c6c6')

    depends_on('libxml2',     type=('build', 'run'))
    depends_on('libxslt',     type=('build', 'run'))
    depends_on('docbook-xml', type=('build', 'run'))
    depends_on('docbook-xsl', type=('build', 'run'))
    depends_on('python@2.3.0:2.7', when='@:8.6.9', type=('build', 'run'))
    depends_on('python@3.5:',      when='@9.0.2:', type=('build', 'run'))

    @when('@:8.6.9')
    def install(self, spec, prefix):
        # Old release demands python2
        mpythpath = spec['python'].command.path
        exes = ['asciidoc', 'a2x']
        for exe in exes:
            fthfile = FileFilter(exe + '.py')
            fthfile.filter('#!/usr/bin/env python', '#!' + mpythpath)

        make('install')
