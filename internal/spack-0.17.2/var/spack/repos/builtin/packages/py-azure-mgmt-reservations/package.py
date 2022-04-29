# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAzureMgmtReservations(PythonPackage):
    """Microsoft Azure Reservations Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-reservations/azure-mgmt-reservations-0.7.0.zip"

    version('0.7.0', sha256='f65c1985a47e0ac55e7d5d9cc1bd5e95335a111566edc289d460aa2bc8f80991')
    version('0.6.0', sha256='83a9a70d6fd78b8b3e92ca64bbc1fde8d1bc5e2efea54076052c51c946b4cc9b')

    depends_on('py-setuptools', type='build')
    depends_on('py-msrest@0.5.0:', type=('build', 'run'))
    depends_on('py-msrestazure@0.4.32:1', type=('build', 'run'))
    depends_on('py-azure-common@1.1:1', type=('build', 'run'))
    depends_on('py-azure-mgmt-nspkg', when='^python@:2', type=('build', 'run'))
