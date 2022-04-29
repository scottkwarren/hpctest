# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyPybtex(PythonPackage):
    """Pybtex is a BibTeX-compatible bibliography processor written in
       Python."""

    homepage = "https://pybtex.org"
    pypi = "pybtex/pybtex-0.24.0.tar.gz"

    version('0.24.0', sha256='818eae35b61733e5c007c3fcd2cfb75ed1bc8b4173c1f70b56cc4c0802d34755')
    version('0.21', sha256='af8a6c7c74954ad305553b118d2757f68bc77c5dd5d5de2cc1fd16db90046000')

    depends_on('python@2.7:2.8,3.3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-latexcodec@1.0.4:', type=('build', 'run'))
    depends_on('py-pyyaml@3.01:', type=('build', 'run'))
    depends_on('py-counter@1:', when='^python@:2.6', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'), when='@0.24.0:')
