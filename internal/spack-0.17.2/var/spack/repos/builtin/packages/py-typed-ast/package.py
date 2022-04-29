# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTypedAst(PythonPackage):
    """A fork of Python 2 and 3 ast modules with type comment support."""

    homepage = "https://github.com/python/typed_ast"
    pypi = "typed-ast/typed_ast-1.4.0.tar.gz"

    version('1.4.3', sha256='fb1bbeac803adea29cedd70781399c99138358c26d05fcbd23c13016b7f5ec65')
    version('1.4.2', sha256='9fc0b3cb5d1720e7141d103cf4819aea239f7d136acf9ee4a69b047b7986175a')
    version('1.4.1', sha256='8c8aaad94455178e3187ab22c8b01a3837f8ee50e09cf31f1ba129eb293ec30b')
    version('1.4.0', sha256='66480f95b8167c9c5c5c87f32cf437d585937970f3fc24386f313a4c97b44e34')

    depends_on('python@3.3:', type=('build', 'link', 'run'))
    depends_on('python@:3.8', when="@:1.4.0")  # build errors with 3.9 until 1.4.1
    depends_on('py-setuptools', type='build')
