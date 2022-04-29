# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyXopen(PythonPackage):
    """This small Python module provides a xopen function that works like the
    built-in open function, but can also deal with compressed files. Supported
    compression formats are gzip, bzip2 and xz. They are automatically
    recognized by their file extensions .gz, .bz2 or .xz."""

    homepage = "https://github.com/marcelm/xopen"
    pypi = "xopen/xopen-0.1.1.tar.gz"

    version('1.0.1', sha256='79d7e425fb0930b0153eb6beba9a540ca3e07ac254ca828577ad2e8fa24105dc')
    version('0.9.0', sha256='1e3918c8a5cd2bd128ba05b3b883ee322349219c99c305e10114638478e3162a')
    version('0.8.4', sha256='dcd8f5ef5da5564f514a990573a48a0c347ee1fdbb9b6374d31592819868f7ba')
    version('0.8.2', sha256='003749e09af74103a29e9c64c468c03e084aa6dfe6feff4fe22366679a6534f7')
    version('0.5.0', sha256='b097cd25e8afec42b6e1780c1f6315016171b5b6936100cdf307d121e2cbab9f')
    version('0.1.1', sha256='d1320ca46ed464a59db4c27c7a44caf5e268301e68319f0295d06bf6a9afa6f3')

    depends_on('python@3.5:', type=('build', 'run'), when='@0.9.0:')
    depends_on('python@2.7,3.4:', type=('build', 'run'), when='@0.5:0.8')
    depends_on('python@2.6:2,3.3:', type=('build', 'run'), when='@0.1.1')
    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')
    depends_on('py-bz2file', type=('build', 'run'), when='@0.5: ^python@:2.8')
