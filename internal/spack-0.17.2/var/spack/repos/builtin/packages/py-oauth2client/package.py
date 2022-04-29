# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyOauth2client(PythonPackage):
    """OAuth 2.0 client library.

    Note: oauth2client is now deprecated. No more features will be added to
    the libraries and the core team is turning down support. We recommend you
    use google-auth and oauthlib."""

    homepage = "https://github.com/google/oauth2client/"
    pypi = "oauth2client/oauth2client-4.1.3.tar.gz"

    version('4.1.3', sha256='d486741e451287f69568a4d26d70d9acd73a2bbfa275746c535b4209891cccc6')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-httplib2@0.9.1:', type=('build', 'run'))
    depends_on('py-pyasn1@0.1.7:', type=('build', 'run'))
    depends_on('py-pyasn1-modules@0.0.5:', type=('build', 'run'))
    depends_on('py-rsa@3.1.4:', type=('build', 'run'))
    depends_on('py-six@1.6.1:', type=('build', 'run'))
