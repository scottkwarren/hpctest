# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyArgcomplete(PythonPackage):
    """Bash tab completion for argparse."""

    homepage = "https://github.com/kislyuk/argcomplete"
    pypi = "argcomplete/argcomplete-1.12.0.tar.gz"

    version('1.12.3', sha256='2c7dbffd8c045ea534921e63b0be6fe65e88599990d8dc408ac8c542b72a5445')
    version('1.12.0', sha256='2fbe5ed09fd2c1d727d4199feca96569a5b50d44c71b16da9c742201f7cc295c')
    version('1.1.1',  sha256='cca45b5fe07000994f4f06a0b95bd71f7b51b04f81c3be0b4ea7b666e4f1f084')

    depends_on('py-setuptools', type='build')
    depends_on('py-importlib-metadata@0.23:4', when='@1.12.3: ^python@:3.7', type=('build', 'run'))
    depends_on('py-importlib-metadata@0.23:1', when='@1.12: ^python@:3.7', type=('build', 'run'))
