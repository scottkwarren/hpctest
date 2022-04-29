# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythonGitlab(PythonPackage):
    """Python wrapper for the GitLab API"""

    homepage = "https://github.com/gpocentek/python-gitlab"
    pypi = "python-gitlab/python-gitlab-0.19.tar.gz"

    version('2.10.1', sha256='7afa7d7c062fa62c173190452265a30feefb844428efc58ea5244f3b9fc0d40f')
    version('1.8.0', sha256='a6b03bc53f6e2e22b88d5ff9772b1bb360570ec82752f1def3d6eb60cda093e7')
    version('0.19',  sha256='88b65591db7a10a0d9979797e4e654a113e2b93b3a559309f6092b27ab93934a')
    version('0.18',  sha256='d60d67c82fedd8c3e4f0bb8b5241bf2df32307c98fdf2f02a94850e21db2d804')
    version('0.17',  sha256='f79337cd8b2343195b7ac0909e0483624d4235cca78fc76196a0ee4e109c9a70')
    version('0.16',  sha256='2c50dc0bd3ed7c6b1edb6e556b0f0109493ae9dfa46e3bffcf3e5e67228d7d53')

    depends_on('python@3.6:', when='@2.0.0:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-requests-toolbelt@0.9.1:', when='@2.6.0:', type=('build', 'run'))
    depends_on('py-requests@2.25.0:', when='@2.10.1:', type=('build', 'run'))
    depends_on('py-requests@2.22.0:', when='@2.0.0:', type=('build', 'run'))
    depends_on('py-requests@2.4.2:', when='@1.4.0:', type=('build', 'run'))
    depends_on('py-requests@1.0:', type=('build', 'run'))
    depends_on('py-six', when='@:1', type=('build', 'run'))
