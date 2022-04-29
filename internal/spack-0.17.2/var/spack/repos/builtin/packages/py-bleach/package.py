# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBleach(PythonPackage):
    """An easy whitelist-based HTML-sanitizing tool."""

    homepage = "https://github.com/mozilla/bleach"
    pypi = "bleach/bleach-3.1.0.tar.gz"

    version('4.1.0', sha256='0900d8b37eba61a802ee40ac0061f8c2b5dee29c1927dd1d233e075ebf5a71da')
    version('4.0.0', sha256='ffa9221c6ac29399cc50fcc33473366edd0cf8d5e2cbbbb63296dc327fb67cc8')
    version('3.3.1', sha256='306483a5a9795474160ad57fce3ddd1b50551e981eed8e15a582d34cef28aafa')
    version('3.1.0', sha256='3fdf7f77adcf649c9911387df51254b813185e32b2c6619f690b593a617e19fa')
    version('1.5.0', sha256='978e758599b54cd3caa2e160d74102879b230ea8dc93871d0783721eef58bc65')

    depends_on('python@3.6:', when='@4.0.0:', type=('build', 'run'))
    depends_on('python@2.7:2,3.5:', when='@3.1.3:', type=('build', 'run'))
    depends_on('python@2.7:2,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-six@1.9.0:', type=('build', 'run'))
    depends_on('py-webencodings', type=('build', 'run'))
    depends_on('py-packaging', when='@3.1.5:', type=('build', 'run'))
