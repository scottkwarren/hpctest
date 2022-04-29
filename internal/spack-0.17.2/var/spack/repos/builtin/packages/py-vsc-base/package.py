# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyVscBase(PythonPackage):
    """Common Python libraries tools created by HPC-UGent"""

    homepage = 'https://github.com/hpcugent/vsc-base/'
    pypi = 'vsc-base/vsc-base-2.5.8.tar.gz'

    version('2.5.8', sha256='7fcd300f842edf4baade7d0b7a3b462ca7dfb2a411a7532694a90127c6646ee2')

    depends_on('py-setuptools', type=('build', 'run'))
