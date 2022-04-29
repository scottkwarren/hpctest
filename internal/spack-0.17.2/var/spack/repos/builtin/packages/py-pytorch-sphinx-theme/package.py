# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPytorchSphinxTheme(PythonPackage):
    """PyTorch Sphinx Theme."""

    homepage = "https://github.com/pytorch/pytorch_sphinx_theme"
    git      = "https://github.com/pytorch/pytorch_sphinx_theme.git"

    version('master', branch='master')

    depends_on('py-setuptools', type='build')
    depends_on('py-sphinx', type=('build', 'run'))
