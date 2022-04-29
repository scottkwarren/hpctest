# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Charliecloud(AutotoolsPackage):
    """Lightweight user-defined software stacks for HPC."""

    maintainers = ['j-ogas', 'reidpr']
    homepage = "https://hpc.github.io/charliecloud"
    url      = "https://github.com/hpc/charliecloud/releases/download/v0.18/charliecloud-0.18.tar.gz"
    git      = "https://github.com/hpc/charliecloud.git"

    tags = ['e4s']

    version('master', branch='master')
    version('0.25',   sha256='62d6fd211e3a573f54578e1b01d5c298f9788b7eaf2db46ac94c2dcef604cc94')
    version('0.24',   sha256='63379bcbad7b90b33457251696d6720416e4acefcf2b49cd6cb495a567e511c2')
    version('0.23',   sha256='5e458b943ad0e27d1264bb089e48d4a676219179b0e96a7d761387a36c45b4d9')
    version('0.22',   sha256='f65e4111ce87e449c656032da69f3b1cfc70a5a416a5e410329c1b0b2e953907')
    version('0.21',   sha256='024884074d283c4a0387d899161610fa4ae739ac1efcc9e53d7d626ddc20359f')
    version('0.19',   sha256='99619fd86860cda18f7f7a7cf7391f702ec9ebd3193791320dea647769996447')
    version('0.18',   sha256='15ce63353afe1fc6bcc10979496a54fcd5628f997cb13c827c9fc7afb795bdc5')

    depends_on('m4',       type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')

    depends_on('python@3.5:',    type='run')
    # Version 0.25+ bundle the preferred lark version.
    depends_on('py-lark-parser', type='run', when='@:0.24')
    depends_on('py-requests',    type='run')

    # Man pages and html docs variant.
    variant('docs', default=False, description='Build man pages and html docs')
    depends_on('rsync',               type='build', when='+docs')
    depends_on('py-sphinx',           type='build', when='+docs')
    depends_on('py-sphinx-rtd-theme', type='build', when='+docs')

    # See https://github.com/spack/spack/pull/16049.
    conflicts('platform=darwin', msg='This package does not build on macOS')

    # Bash automated testing harness (bats).
    depends_on('bats@0.4.0', type='test')

    def configure_args(self):

        args = []
        py_path = self.spec['python'].command.path
        args.append('--with-python={0}'.format(py_path))

        if '+docs' in self.spec:
            sphinx_bin = '{0}'.format(self.spec['py-sphinx'].prefix.bin)
            args.append('--enable-html')
            args.append('--with-sphinx-build={0}'.format(sphinx_bin.join(
                                                         'sphinx-build')))
        else:
            args.append('--disable-html')

        return args
