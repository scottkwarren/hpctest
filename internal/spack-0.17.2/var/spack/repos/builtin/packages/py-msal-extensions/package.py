# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyMsalExtensions(PythonPackage):
    """The Microsoft Authentication Extensions for Python offers secure
    mechanisms for client applications to perform cross-platform token cache
    serialization and persistence. It gives additional support to the
    Microsoft Authentication Library for Python (MSAL)."""

    homepage = "https://github.com/AzureAD/microsoft-authentication-library-for-python"
    pypi = "msal-extensions/msal-extensions-0.2.2.tar.gz"

    version('0.2.2', sha256='31414753c484679bb3b6c6401623eb4c3ccab630af215f2f78c1d5c4f8e1d1a9')
    version('0.1.3', sha256='59e171a9a4baacdbf001c66915efeaef372fb424421f1a4397115a3ddd6205dc')

    depends_on('py-setuptools', type='build')
    depends_on('py-msal@0.4.1:1', type=('build', 'run'))
    depends_on('py-portalocker@1.0:1', type=('build', 'run'))
    depends_on('py-pathlib2', when='@0.2:^python@:2', type=('build', 'run'))
