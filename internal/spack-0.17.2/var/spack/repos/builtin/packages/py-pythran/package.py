# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack import *


class PyPythran(PythonPackage):
    """Ahead of Time compiler for numeric kernels."""

    homepage = "https://github.com/serge-sans-paille/pythran"
    pypi     = "pythran/pythran-0.9.11.tar.gz"

    version('0.9.12', sha256='5d50dc74dca1d3f902941865acbae981fc24cceeb9d54673d68d6b5c8c1b0001')
    version('0.9.11', sha256='a317f91e2aade9f6550dc3bf40b5caeb45b7e012daf27e2b3e4ad928edb01667')
    version('0.9.10', sha256='8fa1d19624cb2950e5a18974fdcb0dffc57e1a821049dc95df09563edd673915')
    version('0.9.9', sha256='aaabc97f30ad46d1d62303323de6697d2933779afa4666c15b0f433cb50825b1')
    version('0.9.8', sha256='81c10a16fce9ed41211fb70e82fda6984e93f4602a164934648db8cbb08156b3')
    version('0.9.7', sha256='ac36a94bd862e3c80dae585158b90d3e7c5c05fd252819f3ca7d880a1c7c1012')
    version('0.9.6', sha256='2d102a55d9d53f77cf0f4a904eeb5cbaa8fe76e4892319a859fc618401e2f6ba')
    version('0.9.5', sha256='815a778d6889593c0b8ddf08052cff36a504ce4cc8bd8d7bfb856a212f91486e')
    version('0.9.4', sha256='ec9c91f5331454263b064027292556a184a9f55a50f8615e09b08f57a4909855')
    version('0.9.3', sha256='217427a8225a331fdc8f3efe57871aed775cdf2c6e847a0a83df0aaae4b02493')

    depends_on('python@3:', when='@0.9.6:', type=('build', 'run'))
    depends_on('python@2.7:', when='@:0.9.5', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-pytest-runner', type='build')
    depends_on('py-ply@3.4:', type=('build', 'run'))
    depends_on('py-networkx@2:', when='@:0.9.11', type=('build', 'run'))
    depends_on('py-decorator', when='@:0.9.11', type=('build', 'run'))
    depends_on('py-gast@0.5.0:0.5', when='@0.9.12:', type=('build', 'run'))
    depends_on('py-gast@0.4.0:0.4', when='@0.9.7:0.9.11', type=('build', 'run'))
    depends_on('py-gast@0.3.3:0.3', when='@0.9.6', type=('build', 'run'))
    depends_on('py-gast@0.3.0:', when='@0.9.4:0.9.5', type=('build', 'run'))
    depends_on('py-gast', when='@:0.9.3', type=('build', 'run'))
    depends_on('py-six', when='@:0.9.11', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-beniget@0.4.0:0.4', when='@0.9.12:', type=('build', 'run'))
    depends_on('py-beniget@0.3.0:0.3', when='@0.9.7:0.9.11', type=('build', 'run'))
    depends_on('py-beniget@0.2.1:0.2', when='@0.9.6', type=('build', 'run'))
    depends_on('py-beniget@0.2.0:', when='@0.9.4:0.9.5', type=('build', 'run'))
    depends_on('py-beniget', when='@:0.9.3', type=('build', 'run'))
    depends_on('llvm-openmp', when='%apple-clang', type=('build', 'run'))

    # https://github.com/serge-sans-paille/pythran/pull/1856
    patch('omp.patch', when='@0.9.10:0.9.12')

    def patch(self):
        # Compiler is used at run-time to determine name of OpenMP library to search for
        cfg_file = join_path('pythran', 'pythran-{0}.cfg'.format(sys.platform))
        filter_file('CXX=', 'CXX=' + self.compiler.cxx, cfg_file)

    def setup_build_environment(self, env):
        # Needed for `spack install --test=root py-pythran`
        if self.spec.satisfies('%apple-clang'):
            env.prepend_path(
                'DYLD_FALLBACK_LIBRARY_PATH',
                self.spec['llvm-openmp'].libs.directories[0]
            )

    def setup_run_environment(self, env):
        # Needed for `spack test run py-pythran`
        self.setup_build_environment(env)

    def setup_dependent_build_environment(self, env, dependent_spec):
        # Needed for `spack install py-scipy`
        self.setup_build_environment(env)

    def setup_dependent_run_environment(self, env, dependent_spec):
        # Probably needed for something?
        self.setup_build_environment(env)
