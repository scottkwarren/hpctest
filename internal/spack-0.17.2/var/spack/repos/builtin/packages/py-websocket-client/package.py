# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyWebsocketClient(PythonPackage):
    """WebSocket client for Python. hybi13 is supported."""

    homepage = "https://github.com/websocket-client/websocket-client.git"
    pypi = "websocket_client/websocket_client-0.57.0.tar.gz"

    version('0.57.0', sha256='d735b91d6d1692a6a181f2a8c9e0238e5f6373356f561bb9dc4c7af36f452010')
    version('0.56.0', sha256='1fd5520878b68b84b5748bb30e592b10d0a91529d5383f74f4964e72b297fd3a')
    version('0.48.0', sha256='18f1170e6a1b5463986739d9fd45c4308b0d025c1b2f9b88788d8f69e8a5eb4a')

    depends_on('python@2.6:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-backports-ssl-match-hostname', when='^python@2.6:2.7.9', type=('build', 'run'))
    depends_on('py-argparse', when='^python@:2.6', type=('build', 'run'))
