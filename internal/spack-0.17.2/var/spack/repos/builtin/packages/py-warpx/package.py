# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyWarpx(PythonPackage):
    """WarpX is an advanced electromagnetic Particle-In-Cell code. It supports
    many features including Perfectly-Matched Layers (PML) and mesh refinement.
    In addition, WarpX is a highly-parallel and highly-optimized code and
    features hybrid OpenMP/MPI parallelization, advanced vectorization
    techniques and load balancing capabilities.

    These are the Python bindings of WarpX with PICMI input support.
    See the C++ 'warpx' package for the WarpX application and library.
    """

    homepage = "https://ecp-warpx.github.io"
    url      = "https://github.com/ECP-WarpX/WarpX/archive/refs/tags/21.04.tar.gz"
    git      = "https://github.com/ECP-WarpX/WarpX.git"

    maintainers = ['ax3l', 'dpgrote', 'RemiLehe']

    tags = ['e4s']

    # NOTE: if you update the versions here, also see warpx
    version('develop', branch='development')
    version('21.11', sha256='ce60377771c732033a77351cd3500b24b5d14b54a5adc7a622767b9251c10d0b')
    version('21.10', sha256='d372c573f0360094d5982d64eceeb0149d6620eb75e8fdbfdc6777f3328fb454')
    version('21.09', sha256='861a65f11846541c803564db133c8678b9e8779e69902ef1637b21399d257eab')
    version('21.08', sha256='6128a32cfd075bc63d08eebea6d4f62d33ce0570f4fd72330a71023ceacccc86')
    version('21.07', sha256='a8740316d813c365715f7471201499905798b50bd94950d33f1bd91478d49561')
    version('21.06', sha256='a26039dc4061da45e779dd5002467c67a533fc08d30841e01e7abb3a890fbe30')
    version('21.05', sha256='f835f0ae6c5702550d23191aa0bb0722f981abb1460410e3d8952bc3d945a9fc')
    version('21.04', sha256='51d2d8b4542eada96216e8b128c0545c4b7527addc2038efebe586c32c4020a0')

    variant('mpi', default=True,
            description='Enable MPI support')

    for v in ['21.11', '21.10', '21.09', '21.08', '21.07', '21.06', '21.05',
              '21.04', 'develop']:
        depends_on('warpx@{0}'.format(v),
                   when='@{0}'.format(v),
                   type=['build', 'link'])

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-numpy@1.15.0:1', type=('build', 'run'))
    depends_on('py-mpi4py@2.0.0:', type=('build', 'run'), when='+mpi')
    depends_on('py-periodictable@1.5:1', type=('build', 'run'))
    depends_on('py-picmistandard@0.0.14', type=('build', 'run'))
    depends_on('py-setuptools@38.6:', type='build')
    depends_on('py-wheel', type='build')
    depends_on('warpx +lib ~mpi +shared', type=('build', 'link'), when='~mpi')
    depends_on('warpx +lib +mpi +shared', type=('build', 'link'), when='+mpi')

    def setup_build_environment(self, env):
        env.set('PYWARPX_LIB_DIR', self.spec['warpx'].prefix.lib)
