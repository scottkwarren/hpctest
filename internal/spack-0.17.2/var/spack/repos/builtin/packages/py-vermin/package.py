# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyVermin(PythonPackage):
    """Concurrently detect the minimum Python versions needed to run code."""

    homepage = "https://github.com/netromdk/vermin"
    url      = "https://github.com/netromdk/vermin/archive/v1.3.2.tar.gz"

    maintainers = ['netromdk']

    version('1.3.2', sha256='2818eaea24c5be5dae1f374ddb2377e9cfaad04d0a3372ad129cffc46cec5404')
    version('1.3.1', sha256='ddcdaad5a708a483af192075f5d2eaaaf3aa4661b5101ddafa40d7837eeb5368')
    version('1.3.0', sha256='adf2b6ea34c01c3a81fc4fa78c2e5fa6c8dd6d35327a8e5a4caeeaef7ec21668')
    version('1.2.2', sha256='d0343b2a78d7e4de67dfd2d882eeaf8b241db724f7e67f83bdd4111edb97f1e2')
    version('1.2.1', sha256='b7b2c77cf67a27a432371cbc7f184151b6f3dd22bd9ccf3a7a10b7ae3532ac81')
    version('1.2.0', sha256='a3ab6dc6608b859f301b9a77d5cc0d03335aae10c49d47a91b82be5be48c4f1f')
    version('1.1.1', sha256='d13b2281ba16c9d5b0913646483771789552230a9ed625e2cd92c5a112e4ae80')
    version('1.1.0', sha256='62d9f1b6694f50c22343cead2ddb6e2b007d24243fb583f61ceed7540fbe660b')
    version('1.0.3', sha256='1503be05b55cacde1278a1fe55304d8ee889ddef8ba16e120ac6686259bec95c')
    version('1.0.2', sha256='e999d5f5455e1116b366cd1dcc6fecd254c7ae3606549a61bc044216f9bb5b55')
    version('1.0.1', sha256='c06183ba653b9d5f6687a6686da8565fb127fab035f9127a5acb172b7c445079')
    version('1.0.0', sha256='e598e9afcbe3fa6f3f3aa894da81ccb3954ec9c0783865ecead891ac6aa57207')
    version('0.10.5', sha256='00601356e8e10688c52248ce0acc55d5b45417b462d5aa6887a6b073f0d33e0b')
    version('0.10.4', sha256='bd765b84679fb3756b26f462d2aab4af3183fb65862520afc1517f6b39dea8bf')
    version('0.10.0', sha256='3458a4d084bba5c95fd7208888aaf0e324a07ee092786ee4e5529f539ab4951f')

    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))

    @run_after('build')
    @on_package_attributes(run_tests=True)
    def build_test(self):
        make('test')
