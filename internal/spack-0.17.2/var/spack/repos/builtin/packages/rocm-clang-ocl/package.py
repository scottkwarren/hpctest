# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RocmClangOcl(CMakePackage):
    """ OpenCL compilation with clang compiler """

    homepage = "https://github.com/RadeonOpenCompute/clang-ocl"
    git      = "https://github.com/RadeonOpenCompute/clang-ocl.git"
    url      = "https://github.com/RadeonOpenCompute/clang-ocl/archive/rocm-4.3.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']
    version('master', branch='master')
    version('4.3.1', sha256='12461d4fd4f3f40710d2c041cfee37da83ccda9d2761d7708335349e7ec5ad87')
    version('4.3.0', sha256='bc5650f2f105b10a1e22d8e5cc9464b0f960252a08e5e1fdee222af1fc5c022c')
    version('4.2.0', sha256='702796f4e31f6119173d915db9bee13c060a75d9eb5b1f8e3d20779d6702dfdc')
    version('4.1.0', sha256='c6e65da5541df9ee940caeeffe1b87c92547edc1770538fd2010c9c998a593b5')
    version('4.0.0', sha256='c8f9091396ee0096f6d7c1cd13d80532c424e838bec1e4cebf903ebaf649e82e')
    version('3.10.0', sha256='17fc8fb8c38b18f9f0cac339dda6cea3e9e66805f7a92ec2456072fc1e72fa85')
    version('3.9.0', sha256='3d63c7ac259ba8b0bfd5e4a94df1490c2b6cbac4d43dc7bbc210a536251268fe')
    version('3.8.0', sha256='a829aa2efb6e3bc00d8a08a96404f937f3c8adf3b4922b5ac35050d6e08b912d')
    version('3.7.0', sha256='9c00c7e7dd3ac8326ae6772a43866b44ae049d5960ea6993d14a2370db74d326')
    version('3.5.0', sha256='38c95fbd0ac3d11d9bd224ad333b68b9620dde502b8a8a9f3d96ba642901e8bb')

    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')

    depends_on('cmake@3:', type='build')

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1', 'master']:
        depends_on('rocm-cmake@' + ver, type='build', when='@' + ver)
        depends_on('llvm-amdgpu@' + ver,              when='@' + ver)

        # support both builtin and standalone device libs
        depends_on('rocm-device-libs@' + ver, when='@{0} ^llvm-amdgpu ~rocm-device-libs'.format(ver))
