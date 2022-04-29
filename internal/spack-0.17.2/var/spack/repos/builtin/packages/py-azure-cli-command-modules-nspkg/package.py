# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAzureCliCommandModulesNspkg(PythonPackage):
    """Microsoft Azure CLI Command Modules Namespace Package."""

    homepage = "https://github.com/Azure/azure-cli"
    pypi = "azure-cli-command-modules-nspkg/azure-cli-command-modules-nspkg-2.0.3.tar.gz"

    version('2.0.3', sha256='4bd62bf5facb92dd4f89080e75eaee2ea1d3dd4e57a3d2a760ce501cf53f4e7d')

    depends_on('py-setuptools', type='build')
    depends_on('py-azure-cli-nspkg@3.0.0:', type=('build', 'run'))
