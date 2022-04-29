# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRtree(PythonPackage):
    """R-Tree spatial index for Python GIS."""

    homepage = "https://github.com/Toblerity/rtree"
    pypi = "Rtree/Rtree-0.8.3.tar.gz"

    version('0.9.7', sha256='be8772ca34699a9ad3fb4cfe2cfb6629854e453c10b3328039301bbfc128ca3e')
    version('0.8.3', sha256='6cb9cf3000963ea6a3db777a597baee2bc55c4fc891e4f1967f262cc96148649')

    depends_on('python@3:', when='@0.9.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-wheel', when='@0.9.4:', type='build')
    depends_on('libspatialindex@1.8.5:')

    def setup_build_environment(self, env):
        env.set('SPATIALINDEX_C_LIBRARY', self.spec['libspatialindex'].libs[0])

    def setup_run_environment(self, env):
        self.setup_build_environment(env)
