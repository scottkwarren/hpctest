# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAzureNspkg(PythonPackage):
    """Microsoft Azure Namespace Package [Internal]."""

    homepage = "hhttps://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-nspkg/azure-nspkg-3.0.2.zip"

    version('3.0.2', sha256='e7d3cea6af63e667d87ba1ca4f8cd7cb4dfca678e4c55fc1cedb320760e39dd0')

    depends_on('py-setuptools', type='build')
