# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hive(Package):
    """
    The Apache Hive data warehouse software facilitates reading, writing,
    and managing large datasets residing in distributed storage using SQL.
    Structure can be projected onto data already in storage. A command line
    tool and JDBC driver are provided to connect users to Hive.
    """

    homepage = "https://hive.apache.org/"
    url      = "https://www.apache.org/dist/hive/hive-3.1.2/apache-hive-3.1.2-bin.tar.gz"

    version('3.1.2', sha256='d75dcf36908b4e7b9b0ec9aec57a46a6628b97b276c233cb2c2f1a3e89b13462')
    version('2.3.6', sha256='0b3736edc8d15f01ed649bfce7d74346c35fd57567411e9d0c3f48578f76610d')
    version('1.2.2', sha256='763b246a1a1ceeb815493d1e5e1d71836b0c5b9be1c4cd9c8d685565113771d1')

    depends_on('hadoop', type='run')

    def install(self, spec, prefix):
        install_tree('.', prefix)
