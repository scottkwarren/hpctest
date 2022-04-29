# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythonLdap(PythonPackage):
    """python-ldap provides an object-oriented API to access LDAP directory
    servers from Python programs.
    """

    homepage = "https://www.python-ldap.org/en/python-ldap-3.2.0/"
    pypi = "python-ldap/python-ldap-3.2.0.tar.gz"

    version('3.2.0', sha256='7d1c4b15375a533564aad3d3deade789221e450052b21ebb9720fb822eccdb8e')
    version('3.0.0', sha256='86746b912a2cd37a54b06c694f021b0c8556d4caeab75ef50435ada152e2fbe1')

    depends_on('openldap+client_only', type=('build', 'link', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-pyasn1@0.3.7:', type=('build', 'run'))
    depends_on('py-pyasn1-modules@0.1.5:', type=('build', 'run'))
    depends_on('cyrus-sasl', type='link')
