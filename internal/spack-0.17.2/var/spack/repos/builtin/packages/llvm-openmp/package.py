# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class LlvmOpenmp(CMakePackage):
    """The OpenMP subproject of LLVM contains the components required to build
    an executable OpenMP program that are outside the compiler itself."""

    homepage = "https://openmp.llvm.org/"
    url      = "https://releases.llvm.org/9.0.0/openmp-9.0.0.src.tar.xz"

    version('12.0.1', sha256='60fe79440eaa9ebf583a6ea7f81501310388c02754dbe7dc210776014d06b091')
    version('9.0.0', sha256='9979eb1133066376cc0be29d1682bc0b0e7fb541075b391061679111ae4d3b5b')
    version('8.0.0', sha256='f7b1705d2f16c4fc23d6531f67d2dd6fb78a077dd346b02fed64f4b8df65c9d5')

    depends_on('cmake@2.8:', type='build')

    variant('multicompat', default=False,
            description="Support gomp and the Intel openMP runtime library.")

    def url_for_version(self, version):
        if version >= Version('9.0.1'):
            url = "https://github.com/llvm/llvm-project/releases/download/llvmorg-{0}/openmp-{0}.src.tar.xz"
        else:
            url = "https://releases.llvm.org/{0}/openmp-{0}.src.tar.xz"

        return url.format(version.dotted)

    def cmake_args(self):

        # Disable LIBOMP_INSTALL_ALIASES, otherwise the library is installed as
        # libgomp alias which can conflict with GCC's libgomp.
        cmake_args = [
            '-DLIBOMP_INSTALL_ALIASES=OFF'
        ]
        # Add optional support for both Intel and gcc compilers
        if self.spec.satisfies('+multicompat'):
            cmake_args.append('-DKMP_GOMP_COMPAT=1')
        return cmake_args

    @property
    def libs(self):
        return find_libraries('libomp', root=self.prefix, recursive=True)
