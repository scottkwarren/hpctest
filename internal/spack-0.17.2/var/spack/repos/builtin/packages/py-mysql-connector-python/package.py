# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMysqlConnectorPython(PythonPackage):
    """MySQL Connector/Python is implementing the MySQL Client/Server
    protocol completely in Python. No MySQL libraries are needed, and
    no compilation is necessary to run this Python DB API v2.0
    compliant driver."""

    homepage = "https://github.com/mysql/mysql-connector-python"
    url      = "https://github.com/mysql/mysql-connector-python/archive/8.0.13.tar.gz"
    git      = "https://github.com/mysql/mysql-connector-python.git"

    version('8.0.13', sha256='d4c0834c583cdb90c0aeae90b1917d58355a4bf9b0266c16fd58874a5607f9d4')

    # Fix `error: option --single-version-externally-managed not recognized`
    # https://github.com/mysql/mysql-connector-python/pull/9
    patch('single-version.patch')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-protobuf@3.0.0:', type=('build', 'run'))
