# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySympy(PythonPackage):
    """SymPy is a Python library for symbolic mathematics."""
    pypi = "sympy/sympy-0.7.6.tar.gz"

    version('1.8',     sha256='1ca588a9f6ce6a323c5592f9635159c2093572826668a1022c75c75bdf0297cb')
    version('1.7.1',   sha256='a3de9261e97535b83bb8607b0da2c7d03126650fafea2b2789657b229c246b2e')
    version('1.7',     sha256='9104004669cda847f38cfd8cd16dd174952c537349dbae740fea5331d2b3a51b')
    version('1.6.2',   sha256='1cfadcc80506e4b793f5b088558ca1fcbeaec24cd6fc86f1fdccaa3ee1d48708')
    version('1.6.1',   sha256='7386dba4f7e162e90766b5ea7cab5938c2fe3c620b310518c8ff504b283cb15b')
    version('1.6',     sha256='9769e3d2952e211b1245f1d0dfdbfbdde1f7779a3953832b7dd2b88a21ca6cc6')
    version('1.5.1',   sha256='d77901d748287d15281f5ffe5b0fef62dd38f357c2b827c44ff07f35695f4e7e')
    version('1.5',     sha256='31567dc010bff0967ef7a87210acf3f938c6ab24481581fc143536fb103e9ce8')
    version('1.4', sha256='71a11e5686ae7ab6cb8feb5bd2651ef4482f8fd43a7c27e645a165e4353b23e1')
    version('1.3', sha256='e1319b556207a3758a0efebae14e5e52c648fc1db8975953b05fff12b6871b54')
    version('1.1.1', sha256='ac5b57691bc43919dcc21167660a57cc51797c28a4301a6144eff07b751216a4')
    version('1.0', sha256='3eacd210d839e4db911d216a9258a3ac6f936992f66db211e22767983297ffae')
    version('0.7.6', sha256='dfa3927e9befdfa7da7a18783ccbc2fe489ce4c46aa335a879e49e48fc03d7a7')

    depends_on('python@2.7:2.8,3.4:', when='@:1.4', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.5:', when='@1.5', type=('build', 'run'))
    depends_on('python@3.5:', when='@1.6', type=('build', 'run'))
    depends_on('python@3.6:', when='@1.7:', type=('build', 'run'))

    depends_on('py-mpmath@0.19:', when='@1.0:', type=('build', 'run'))
