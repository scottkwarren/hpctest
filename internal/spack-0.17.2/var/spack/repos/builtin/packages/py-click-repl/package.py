# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class PyClickRepl(PythonPackage):
    """Subcommand REPL for click apps """

    homepage = "https://github.com/click-contrib/click-repl"
    pypi = "click-repl/click-repl-0.1.6.tar.gz"

    version('0.1.6', sha256='b9f29d52abc4d6059f8e276132a111ab8d94980afe6a5432b9d996544afa95d5')

    depends_on('python@3.0:', type=('build', 'run'))
    depends_on('py-click', type=('build', 'run'))
    depends_on('py-prompt-toolkit', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
