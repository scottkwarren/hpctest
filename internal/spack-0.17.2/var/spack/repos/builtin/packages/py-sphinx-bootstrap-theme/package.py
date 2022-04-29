# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySphinxBootstrapTheme(PythonPackage):
    """Sphinx Bootstrap Theme."""

    pypi = "sphinx-bootstrap-theme/sphinx-bootstrap-theme-0.4.13.tar.gz"

    version('0.4.13', sha256='47f7719e56304026f285455bbb115525d227a6e23341d4b7f6f0b48b2eface82')

    depends_on('py-setuptools', type='build')
