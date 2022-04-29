# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyEspressopp(CMakePackage):
    """ESPResSo++ is an extensible, flexible, fast and parallel simulation
       software for soft matter research. It is a highly versatile software
       package for the scientific simulation and analysis of coarse-grained
       atomistic or bead-spring models as they are used in soft matter research
    """
    homepage = "https://espressopp.github.io"
    url      = "https://github.com/espressopp/espressopp/tarball/v3.0.0"
    git      = "https://github.com/espressopp/espressopp.git"

    version('master', branch='master')
    version('3.0.0', sha256='63518e768a98179ad5ef3be96eabaa4d38063b34962e2278db7d59ed2bb8a32e')
    version('2.0.2',   sha256='8cf4525bca06426379f5b9fbb8cc2603f559d28a2e74d1d7694df963b8f3dc6c', deprecated=True)
    version('1.9.5',   sha256='8093f1a226f9fee8fb37c401767439a29ff3656dede3a44b4160169fc90d4d91', deprecated=True)

    variant('ug', default=False, description='Build user guide')
    variant('pdf', default=False, description='Build user guide in pdf format')
    variant('dg', default=False, description='Build developer guide')

    depends_on("cmake@2.8:", type='build')
    depends_on("mpi")
    depends_on("boost+serialization+filesystem+system+python+mpi cxxstd=11")
    depends_on("boost+numpy cxxstd=11", when="@master")
    extends("python")
    depends_on("python@2:2.8", when="@:2", type=('build', 'run'))
    depends_on("python@3:", type=('build', 'run'))
    depends_on("py-mpi4py@2.0.0:", type=('build', 'run'))
    depends_on("fftw")
    depends_on("py-sphinx", when="+ug", type='build')
    depends_on("py-sphinx", when="+pdf", type='build')
    depends_on('py-numpy@:1.16.6', when='@:2', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-pyh5md', when='@master', type=('build', 'run'))
    depends_on('py-matplotlib', when="+ug", type='build')
    depends_on('py-matplotlib', when="+pdf", type='build')
    depends_on("texlive", when="+pdf", type='build')
    depends_on("doxygen", when="+dg", type='build')

    def cmake_args(self):
        return [
            '-DEXTERNAL_MPI4PY=ON',
            '-DEXTERNAL_BOOST=ON',
            '-DWITH_RC_FILES=OFF'
        ]

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            make()
            if '+ug' in spec:
                make("ug", parallel=False)
            if '+pdf' in spec:
                make("ug-pdf", parallel=False)
            if '+dg' in spec:
                make("doc", parallel=False)
