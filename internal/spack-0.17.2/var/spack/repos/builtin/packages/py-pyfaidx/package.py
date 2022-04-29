# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyfaidx(PythonPackage):
    """pyfaidx: efficient pythonic random access to fasta subsequences"""

    pypi = "pyfaidx/pyfaidx-0.5.5.2.tar.gz"

    version('0.5.5.2', sha256='9ac22bdc7b9c5d995d32eb9dc278af9ba970481636ec75c0d687d38c26446caa')

    depends_on('py-setuptools@0.7:', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-ordereddict', type=('build', 'run'), when='^python@:2.6')
    depends_on('py-argparse', type=('build', 'run'), when='^python@:2.6')
