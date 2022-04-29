# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPackaging(PythonPackage):
    """Core utilities for Python packages."""

    homepage = "https://github.com/pypa/packaging"
    pypi = "packaging/packaging-19.2.tar.gz"

    version('21.0', sha256='7dc96269f53a4ccec5c0670940a4281106dd0bb343f47b7471f779df49c2fbe7')
    version('20.9', sha256='5b327ac1320dc863dca72f4514ecc086f31186744b84a230374cc1fd776feae5')
    version('19.2', sha256='28b924174df7a2fa32c1953825ff29c61e2f5e082343165438812f00d3a7fc47')
    version('19.1', sha256='c491ca87294da7cc01902edbe30a5bc6c4c28172b5138ab4e4aa1b9d7bfaeafe')
    version('19.0', sha256='0c98a5d0be38ed775798ece1b9727178c4469d9c3b4ada66e8e6b7849f8732af')
    version('17.1', sha256='f019b770dd64e585a99714f1fd5e01c7a8f11b45635aa953fd41c689a657375b')
    version('16.8', sha256='5d50835fdf0a7edf0b55e311b7c887786504efea1177abd7e69329a8e5ea619e')

    depends_on('python@3.4:', when='@21:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools@40.8.0:', when='@20.8:', type='build')
    depends_on('py-setuptools', type='build')

    depends_on('py-pyparsing@2.0.2:', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'), when='@:20.7')
    depends_on('py-attrs', type=('build', 'run'), when='@19.1')
