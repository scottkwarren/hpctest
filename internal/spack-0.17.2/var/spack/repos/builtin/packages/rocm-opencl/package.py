# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RocmOpencl(CMakePackage):
    """OpenCL: Open Computing Language on ROCclr"""

    homepage = "https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime"
    git      = "https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime.git"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    def url_for_version(self, version):
        if version == Version('3.5.0'):
            return "https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime/archive/roc-3.5.0.tar.gz"

        url = "https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime/archive/rocm-{0}.tar.gz"
        return url.format(version)
    version('master', branch='main')
    version('4.3.1', sha256='7f98f7d4707b4392f8aa7017aaca9e27cb20263428a1a81fb7ec7c552e60c4ca')
    version('4.3.0', sha256='d37bddcc6835b6c0fecdf4d02c204ac1d312076f3eef2b1faded1c4c1bc651e9')
    version('4.2.0', sha256='18133451948a83055ca5ebfb5ba1bd536ed0bcb611df98829f1251a98a38f730')
    version('4.1.0', sha256='0729e6c2adf1e3cf649dc6e679f9cb936f4f423f4954ad9852857c0a53ef799c')
    version('4.0.0', sha256='d43ea5898c6b9e730b5efabe8367cc136a9260afeac5d0fe85b481d625dd7df1')
    version('3.10.0', sha256='3aa9dc5a5f570320b04b35ee129ce9ff21062d2770df934c6c307913f975e93d')
    version('3.9.0', sha256='286ff64304905384ce524cd8794c28aee216befd6c9267d4187a12e5a21e2daf')
    version('3.8.0', sha256='7f75dd1abf3d771d554b0e7b0a7d915ab5f11a74962c92b013ee044a23c1270a')
    version('3.7.0', sha256='283e1dfe4c3d2e8af4d677ed3c20e975393cdb0856e3ccd77b9c7ed2a151650b')
    version('3.5.0', sha256='511b617d5192f2d4893603c1a02402b2ac9556e9806ff09dd2a91d398abf39a0')

    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')

    depends_on('cmake@3:', type='build')
    depends_on('mesa18~llvm@18.3:', type='link')
    depends_on('numactl', type='link', when='@3.7.0:')

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1', 'master']:
        depends_on('hip-rocclr@' + ver, type='build', when='@' + ver)
        depends_on('comgr@' + ver, type='build', when='@' + ver)
        depends_on('hsa-rocr-dev@' + ver, type='link', when='@' + ver)

    def flag_handler(self, name, flags):
        # The includes are messed up in ROCm 3.5.0:
        # ROCM-OpenCL-Runtime uses flat includes
        # and the find_package(ROCclr) bit it
        # commented out. So instead we provide
        # all the includes...

        if name in ('cflags', 'cxxflags'):
            rocclr = self.spec['hip-rocclr'].prefix
            extra_includes = [
                'include',
                'include/compiler/lib/include',
                'include/elf',
                'compiler/lib',
                'compiler/lib/include',
                'elf/utils/libelf',
                'elf/utils/common'
            ]

            for p in extra_includes:
                flag = '-I {0}'.format(join_path(rocclr, p))
                flags.append(flag)

        return (flags, None, None)

    def cmake_args(self):

        args = [
            '-DUSE_COMGR_LIBRARY=yes',
            '-DROCclr_DIR={0}'.format(self.spec['hip-rocclr'].prefix),
            '-DLIBROCclr_STATIC_DIR={0}/lib'.format
            (self.spec['hip-rocclr'].prefix)
        ]
        return args

    def setup_run_environment(self, env):
        env.set('OCL_ICD_VENDORS', self.prefix.vendors + '/')

    @run_after('install')
    def post_install(self):
        vendor_config_path = join_path(self.prefix + '/vendors')
        mkdirp(vendor_config_path)

        config_file_name = 'amdocl64_30800.icd'
        with open(join_path(vendor_config_path, config_file_name), 'w') as f:
            f.write('libamdocl64.so')
