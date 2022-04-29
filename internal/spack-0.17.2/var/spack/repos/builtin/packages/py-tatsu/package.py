# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTatsu(PythonPackage):
    """TatSu (the successor to Grako) is a tool that takes grammars in
    a variation of EBNF as input, and outputs memoizing (Packrat) PEG
    parsers in Python."""

    homepage = "https://github.com/neogeny/tatsu"
    pypi = "TatSu/TatSu-4.4.0.zip"

    version('4.4.0', sha256='80713413473a009f2081148d0f494884cabaf9d6866b71f2a68a92b6442f343d')

    variant('future_regex', default=True, description='Use regex implementation')

    depends_on('python@3.6:', type=('build', 'run'), when='@4.5:')
    depends_on('py-setuptools', type='build')
    # part of the standard lib in python@3.7.0, required in the current HEAD
    depends_on('py-dataclasses@0.6:', type=('build', 'run'), when='@4.5:^python@:3.6')
    # optional dependency, otherwise falls back to standard implementation
    depends_on('py-regex@2018.8:', type=('build', 'run'), when='+future_regex')
