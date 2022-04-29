# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Minio(MakefilePackage):
    """MinIO is a High Performance Object Storage released under Apache
    License v2.0. It is API compatible with Amazon S3 cloud storage
    service. Use MinIO to build high performance infrastructure for
    machine learning, analytics and application data workloads."""

    homepage = "https://min.io/"
    url      = "https://github.com/minio/minio/archive/RELEASE.2020-07-13T18-09-56Z.tar.gz"

    version('2020-07-13T18-09-56Z', sha256='147fca3930389162cc7306a0fa5cf478ee2deba4b31a9317f3d35e82aa58d41e')
    version('2020-07-12T19-14-17Z', sha256='bb8ba5d93215ab37788171d8b9ce68e78d64e7b7c74aea508c15958158d85b03')
    version('2020-07-02T00-15-09Z', sha256='4255c4d95a3e010f16a3f1e974768dc68509075403a97a9b9882f7d9e89fedc5')

    depends_on('go', type='build')

    def url_for_version(self, version):
        return ("https://github.com/minio/minio/archive/RELEASE.{0}.tar.gz".format(version))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('minio', prefix.bin)
