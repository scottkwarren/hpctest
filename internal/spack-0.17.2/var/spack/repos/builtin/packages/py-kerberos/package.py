# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyKerberos(PythonPackage):
    """This Python package is a high-level wrapper for Kerberos
    (GSSAPI) operations. The goal is to avoid having to build a module
    that wraps the entire Kerberos.framework, and instead offer a
    limited set of functions that do what is needed for client/server
    Kerberos authentication based on
    <https://www.ietf.org/rfc/rfc4559.txt>."""

    homepage = "https://github.com/apple/ccs-pykerberos"
    pypi = "kerberos/kerberos-1.3.0.tar.gz"

    version('1.3.0', sha256='f039b7dd4746df56f6102097b3dc250fe0078be75130b9dc4211a85a3b1ec6a4')

    depends_on('py-setuptools', type='build')
    depends_on('keyutils')
    depends_on('krb5@1.3.0:')
