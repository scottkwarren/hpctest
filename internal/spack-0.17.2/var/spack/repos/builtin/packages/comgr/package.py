# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Comgr(CMakePackage):
    """This provides various Lightning Compiler related services. It currently
       contains one library, the Code Object Manager (Comgr)"""

    homepage = "https://github.com/RadeonOpenCompute/ROCm-CompilerSupport"
    git      = "https://github.com/RadeonOpenCompute/ROCm-CompilerSupport.git"
    url      = "https://github.com/RadeonOpenCompute/ROCm-CompilerSupport/archive/rocm-4.3.1.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala', 'haampie']

    version('master', branch='amd-stg-open')
    version('4.3.1', sha256='f1d99550383ed7b3a01d304eedc3d86a8e45b271aa5a80b1dd099c22fda3f745')
    version('4.3.0', sha256='f77b505abb474078374701dfc49e651ad3eeec5349ce6edda54549943a3775ee')
    version('4.2.0', sha256='40a1ea50d2aea0cf75c4d17cdd6a7fe44ae999bf0147d24a756ca4675ce24e36')
    version('4.1.0', sha256='ffb625978555c63582aa46857672431793261166aa31761eff4fe5c2cab661ae')
    version('4.0.0', sha256='f389601fb70b2d9a60d0e2798919af9ddf7b8376a2e460141507fe50073dfb31')
    version('3.10.0', sha256='b44ee5805a6236213d758fa4b612bb859d8f774b9b4bdc3a2699bb009dd631bc')
    version('3.9.0', sha256='6600e144d72dadb6d893a3388b42af103b9443755ce556f4e9e205ccd8ec0c83')
    version('3.8.0', sha256='62a35480dfabaa98883d91ed0f7c490daa9bbd424af37e07e5d85a6e8030b146')
    version('3.7.0', sha256='73e56ec3c63dade24ad351e9340e2f8e127694028c1fb7cec5035376bf098432')
    version('3.5.0', sha256='25c963b46a82d76d55b2302e0e18aac8175362656a465549999ad13d07b689b9')

    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')

    # Disable the hip compile tests.  Spack should not be using
    # /opt/rocm, and this breaks the build when /opt/rocm exists.
    patch('hip-tests.patch', when='@:4.2.0')

    depends_on('cmake@3.2.0:',  type='build', when='@:3.8')
    depends_on('cmake@3.13.4:', type='build', when='@3.9.0:')

    depends_on('zlib', type='link')
    depends_on('z3', type='link')
    depends_on('ncurses', type='link')

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1', 'master']:
        # llvm libs are linked statically, so this *could* be a build dep
        depends_on('llvm-amdgpu@' + ver, when='@' + ver)

        # aomp may not build rocm-device-libs as part of llvm-amdgpu, so make
        # that a conditional dependency
        depends_on('rocm-device-libs@' + ver, when='@{0} ^llvm-amdgpu ~rocm-device-libs'.format(ver))
        depends_on('rocm-cmake@' + ver, type='build', when='@' + ver)

    root_cmakelists_dir = join_path('lib', 'comgr')
