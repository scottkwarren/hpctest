# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyGlobusSdk(PythonPackage):
    """
    Globus SDK for Python
    """

    homepage = "https://github.com/globus/globus-sdk-python"
    pypi     = "globus-sdk/globus-sdk-3.0.2.tar.gz"

    maintainers = ['hategan']

    version('3.0.2', sha256='765b577b37edac70c513179607f1c09de7b287baa855165c9dd68de076d67f16')

    depends_on('python@3.4:', type=('build', 'run'))
    depends_on('py-requests@2.19.1:2', type=('run', 'test'))
    depends_on('py-cryptography@2.0:3.3,3.4.1:3.6', type=('run', 'test'))
    depends_on('py-pyjwt@2.0.0:2+crypto', type=('run', 'test'))
