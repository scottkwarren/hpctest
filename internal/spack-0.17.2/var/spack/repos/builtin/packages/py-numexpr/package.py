# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNumexpr(PythonPackage):
    """Fast numerical expression evaluator for NumPy"""

    homepage = "https://github.com/pydata/numexpr"
    url      = "https://github.com/pydata/numexpr/archive/v2.7.0.tar.gz"

    version('2.7.3', sha256='00d6b1518605afe0ed10417e0ff07123e5d531c02496c6eed7dd4b9923238e1e')
    version('2.7.2', sha256='7d1b3790103221feda07f4a93a4fa5c6654f46865197a677ca6f27eb5cb4e5ef')
    version('2.7.0', sha256='1923f038b90cc69635871968ed742be7775c879451c612f173c2547c823c9561')
    version('2.6.9', sha256='d57267bbdf10906f5ed7841b3484bec4af0494102b50e89ba316924cc7a7fd46')
    version('2.6.5', sha256='fe78a78e002806e87e012b6105f3b3d52d47fc7a72bafb56341fcec7ce02cfd7')
    version('2.6.1', sha256='e92c83d066fa8da63864d69b5f218287cc31437ae844db77390f2183123aab22')
    version('2.5',   sha256='4ca111a9a27c9513c2e2f5b70c0a84ea69081d7d8e4512d4c3f26a485292de0d')
    version('2.4.6', sha256='2681faf55a3f19ba4424cc3d6f0a10610ebd49f029f8453f0ba64dd5c0fe4e0f')

    depends_on('python@2.7:', when='@2.7.3:', type=('build', 'run'))
    depends_on('python@2.6:', when='@:2.7.2', type=('build', 'run'))
    depends_on('py-numpy@1.7:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
