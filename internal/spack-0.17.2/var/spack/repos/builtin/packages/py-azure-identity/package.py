# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAzureIdentity(PythonPackage):
    """Microsoft Azure Identity Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/identity/azure-identity"
    pypi = "azure-identity/azure-identity-1.3.1.zip"

    # 'azure.identity.aio' import doesn't work for some reason, leave out of
    # 'import_modules' list to ensure that tests still pass for other imports.
    import_modules = [
        'azure.identity', 'azure.identity._internal', 'azure.identity._credentials'
    ]

    version('1.3.1', sha256='5a59c36b4b05bdaec455c390feda71b6495fc828246593404351b9a41c2e877a')
    version('1.2.0', sha256='b32acd1cdb6202bfe10d9a0858dc463d8960295da70ae18097eb3b85ab12cb91')

    depends_on('py-setuptools', type='build')
    depends_on('py-azure-core@1.0.0:1', type=('build', 'run'))
    depends_on('py-cryptography@2.1.4:', type=('build', 'run'))
    depends_on('py-msal@1.0.0:1', type=('build', 'run'))
    depends_on('py-msal-extensions@0.1.3:0.1', type=('build', 'run'))
    depends_on('py-six@1.6:', type=('build', 'run'))
    depends_on('py-azure-nspkg', when='^python@:2', type=('build', 'run'))
    depends_on('py-mock', when='^python@:3.2', type=('build', 'run'))
    depends_on('py-typing', when='^python@:3.4', type=('build', 'run'))
