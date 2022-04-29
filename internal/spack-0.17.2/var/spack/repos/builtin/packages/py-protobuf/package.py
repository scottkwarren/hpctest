# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyProtobuf(PythonPackage):
    """Protocol buffers are Google's language-neutral, platform-neutral,
    extensible mechanism for serializing structured data - think XML, but
    smaller, faster, and simpler. You define how you want your data to be
    structured once, then you can use special generated source code to easily
    write and read your structured data to and from a variety of data streams
    and using a variety of languages."""

    homepage = 'https://developers.google.com/protocol-buffers/'
    pypi = 'protobuf/protobuf-3.11.0.tar.gz'

    variant('cpp', default=False,
            description='Enable the cpp implementation')

    version('3.17.3',  sha256='72804ea5eaa9c22a090d2803813e280fb273b62d5ae497aaf3553d141c4fdd7b')
    version('3.17.2',  sha256='5a3450acf046716e4a4f02a3f7adfb7b86f1b5b3ae392cec759915e79538d40d')
    version('3.17.1',  sha256='25bc4f1c23aced9b3a9e70eef7f03e63bcbd6cfbd881a91b5688412dce8992e1')
    version('3.17.0',  sha256='05dfe9319939a8473c21b469f34f6486646e54fb8542637cf7ed8e2fbfe21538')
    version('3.16.0',  sha256='228eecbedd46d75010f1e0f8ce34dbcd11ae5a40c165a9fc9d330a58aa302818')
    version('3.15.8',  sha256='0277f62b1e42210cafe79a71628c1d553348da81cbd553402a7f7549c50b11d0')
    version('3.15.7',  sha256='2d03fc2591543cd2456d0b72230b50c4519546a8d379ac6fd3ecd84c6df61e5d')
    version('3.15.6',  sha256='2b974519a2ae83aa1e31cff9018c70bbe0e303a46a598f982943c49ae1d4fcd3')
    version('3.15.5',  sha256='be8a929c6178bb6cbe9e2c858be62fa08966a39ae758a8493a88f0ed1efb6097')
    version('3.15.1',  sha256='824dbae3390fcc3ea1bf96748e6da951a601802894cf7e1465e72b4732538cab')
    version('3.12.2',  sha256='49ef8ab4c27812a89a76fa894fe7a08f42f2147078392c0dee51d4a444ef6df5')
    version('3.11.2',  sha256='3d7a7d8d20b4e7a8f63f62de2d192cfd8b7a53c56caba7ece95367ca2b80c574')
    version('3.11.1',  sha256='aecdf12ef6dc7fd91713a6da93a86c2f2a8fe54840a3b1670853a2b7402e77c9')
    version('3.11.0',  sha256='97b08853b9bb71512ed52381f05cf2d4179f4234825b505d8f8d2bb9d9429939')
    version('3.10.0',  sha256='db83b5c12c0cd30150bb568e6feb2435c49ce4e68fe2d7b903113f0e221e58fe')
    version('3.9.2',   sha256='843f498e98ad1469ad54ecb4a7ccf48605a1c5d2bd26ae799c7a2cddab4a37ec')
    version('3.9.1',   sha256='d831b047bd69becaf64019a47179eb22118a50dd008340655266a906c69c6417')
    version('3.7.1',   sha256='21e395d7959551e759d604940a115c51c6347d90a475c9baf471a1a86b5604a9')
    version('3.6.1',   sha256='1489b376b0f364bcc6f89519718c057eb191d7ad6f1b395ffd93d1aa45587811')
    version('3.6.0',   sha256='a37836aa47d1b81c2db1a6b7a5e79926062b5d76bd962115a0e615551be2b48d')
    version('3.5.2',   sha256='09879a295fd7234e523b62066223b128c5a8a88f682e3aff62fb115e4a0d8be0')
    version('3.5.1',   sha256='95b78959572de7d7fafa3acb718ed71f482932ddddddbd29ba8319c10639d863')
    version('3.4.0',   sha256='ef02609ef445987976a3a26bff77119c518e0915c96661c3a3b17856d0ef6374')
    version('3.3.0',   sha256='1cbcee2c45773f57cb6de7ee0eceb97f92b9b69c0178305509b162c0160c1f04')
    version('3.1.0',   sha256='0bc10bfd00a9614fae58c86c21fbcf339790e48accf6d45f098034de985f5405',
            url='https://github.com/protocolbuffers/protobuf/releases/download/v3.1.0/protobuf-python-3.1.0.tar.gz',
            deprecated=True)
    version('3.0.0',   sha256='ecc40bc30f1183b418fe0ec0c90bc3b53fa1707c4205ee278c6b90479e5b6ff5')
    version('3.0.0b2', sha256='d5b560bbc4b7d97cc2455c05cad9299d9db02d7bd11193b05684e3a86303c229')
    version('3.0.0a3', sha256='b61622de5048415bfd3f2d812ad64606438ac9e25009ae84191405fe58e522c1')
    version('2.6.1',   sha256='8faca1fb462ee1be58d00f5efb4ca4f64bde92187fe61fde32615bbee7b3e745')
    version('2.5.0',   sha256='58292c459598c9297258bf57acc055f701c727f0154a86af8c0947dde37d8172')
    version('2.4.1',   sha256='df30b98acb6ef892da8b4776175510cff2131908fd0526b6bad960c55a830a1b')
    version('2.3.0',   sha256='374bb047874a506507912c3717d0ce62affbaa9a22bcb494d63d60326a0867b5')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-six@1.9:', when='@3:', type=('build', 'run'))
    depends_on('py-ordereddict', when='@3: ^python@:2', type=('build', 'run'))
    depends_on('py-unittest2', when='@3: ^python@:2', type=('build', 'run'))
    depends_on('protobuf', when='+cpp')

    @property
    def build_directory(self):
        if self.spec.satisfies('@3.1.0'):
            return 'python'
        else:
            return '.'

    @when('+cpp')
    def setup_build_environment(self, env):
        protobuf_dir = self.spec['protobuf'].libs.directories[0]
        env.prepend_path('LIBRARY_PATH', protobuf_dir)

    @when('+cpp')
    def build_args(self, spec, prefix):
        return ['--cpp_implementation']

    @when('+cpp')
    def install_args(self, spec, prefix):
        args = super(PyProtobuf, self).install_args(spec, prefix)
        return args + ['--cpp_implementation']

    @run_after('install')
    def fix_import_error(self):
        if str(self.spec['python'].version.up_to(1)) == '2':
            touch = which('touch')
            touch(self.prefix + '/' +
                  self.spec['python'].package.site_packages_dir +
                  '/google/__init__.py')
