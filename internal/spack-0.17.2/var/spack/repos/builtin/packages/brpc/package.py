# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Brpc(CMakePackage):
    """An industrial-grade RPC framework used throughout Baidu, with
    1,000,000+ instances(not counting clients) and thousands kinds of
    services, called "baidu-rpc" inside Baidu. Only C++ implementatioo
    on is opensourced right now."""

    homepage = "https://github.com/apache/incubator-brpc"
    url      = "https://github.com/apache/incubator-brpc/archive/0.9.7.tar.gz"

    version('0.9.7', sha256='722cd342baf3b05189ca78ecf6c56ea6ffec22e62fc2938335e4e5bab545a49c')
    version('0.9.6', sha256='b872ca844999e0ba768acd823b409761f126590fb34cb0183da915a595161446')
    version('0.9.5', sha256='11ca8942242a4c542c11345b7463a4aea33a11ca33e91d9a2f64f126df8c70e9')

    depends_on('gflags')
    depends_on('protobuf')
    depends_on('leveldb')
    depends_on('openssl')

    patch('narrow.patch', sha256='d7393029443853ddda6c09e3d2185ac2f60920a36a8b685eb83b6b80c1535539', when='@:0.9.7')
