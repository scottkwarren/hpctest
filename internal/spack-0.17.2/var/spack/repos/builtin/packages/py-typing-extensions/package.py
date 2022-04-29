# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTypingExtensions(PythonPackage):
    """The typing_extensions module contains both backports of these
       changes as well as experimental types that will eventually be
       added to the typing module, such as Protocol (see PEP 544 for
       details about protocols and static duck typing)."""

    homepage = "https://github.com/python/typing/tree/master/typing_extensions"
    pypi = "typing_extensions/typing_extensions-3.7.4.tar.gz"

    version('3.10.0.2', sha256='49f75d16ff11f1cd258e1b988ccff82a3ca5570217d7ad8c5f48205dd99a677e')
    version('3.10.0.0', sha256='50b6f157849174217d0656f99dc82fe932884fb250826c18350e159ec6cdf342')
    version('3.7.4.3', sha256='99d4073b617d30288f569d3f13d2bd7548c3a7e4c8de87db09a9d29bb3a4a60c')
    version('3.7.4', sha256='2ed632b30bb54fc3941c382decfd0ee4148f5c591651c9272473fea2c6397d95')
    version('3.7.2', sha256='fb2cd053238d33a8ec939190f30cfd736c00653a85a2919415cecf7dc3d9da71')
    version('3.6.6', sha256='51e7b7f3dcabf9ad22eed61490f3b8d23d9922af400fe6656cb08e66656b701f')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-typing@3.7.4:', when='@3.7: ^python@:3.4', type=('build', 'run'))
    depends_on('py-typing@3.6.2:', when='^python@:3.4', type=('build', 'run'))
