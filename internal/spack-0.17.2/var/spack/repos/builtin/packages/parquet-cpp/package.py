# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ParquetCpp(CMakePackage):
    """C++ bindings for the Apache Parquet columnar data format.
    """

    homepage = "https://github.com/apache/parquet-cpp"
    url = "https://github.com/apache/parquet-cpp/archive/apache-parquet-cpp-1.4.0.tar.gz"

    version('1.4.0', sha256='52899be6c9dc49a14976d4ad84597243696c3fa2882e5c802b56e912bfbcc7ce')

    depends_on('arrow')
    depends_on('boost')
    depends_on('cmake@3.2.0:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('thrift+pic')

    variant('pic', default=True,
            description='Build position independent code')
    variant('build_type', default='Release',
            description='CMake build type',
            values=('Debug', 'FastDebug', 'Release'))

    def cmake_args(self):
        args = ['-DPARQUET_USE_SSE=OFF', '-DPARQUET_BUILD_TESTS=OFF']
        for dep in ('arrow', 'thrift'):
            args.append("-D{0}_HOME={1}".format(dep.upper(),
                                                self.spec[dep].prefix))
        return args

    def flag_handler(self, name, flags):
        flags = list(flags)
        if '+pic' in self.spec:
            if name == 'cflags':
                flags.append(self.compiler.cc_pic_flag)
            elif name == 'cxxflags':
                flags.append(self.compiler.cxx_pic_flag)
        return (None, None, flags)
