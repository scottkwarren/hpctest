# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Z3(CMakePackage):
    """Z3 is a theorem prover from Microsoft Research.
    It is licensed under the MIT license."""

    homepage = "https://github.com/Z3Prover/z3/wiki"
    url      = "https://github.com/Z3Prover/z3/archive/z3-4.5.0.tar.gz"

    version('4.8.9', sha256='c9fd04b9b33be74fffaac3ec2bc2c320d1a4cc32e395203c55126b12a14ff3f4')
    version('4.8.8', sha256='6962facdcdea287c5eeb1583debe33ee23043144d0e5308344e6a8ee4503bcff')
    version('4.8.7', sha256='8c1c49a1eccf5d8b952dadadba3552b0eac67482b8a29eaad62aa7343a0732c3')
    version('4.5.0', sha256='aeae1d239c5e06ac183be7dd853775b84698db1265cb2258e5918a28372d4a0c')

    variant('python', default=False, description='Enable python binding')
    depends_on('python', type='build', when='~python')
    depends_on('python', type=('build', 'run'), when='+python')
    depends_on('py-setuptools', type=('run'), when='+python')
    extends('python', when='+python')

    variant('gmp', default=False, description='GNU multiple precision library support')
    depends_on('cmake@3.4:', type='build')
    depends_on('gmp', when='+gmp', type=('build', 'link'))

    # Referenced: https://github.com/Z3Prover/z3/issues/1016
    patch('fix_1016_2.patch', when='@4.5.0')

    build_directory = 'build'

    def cmake_args(self):
        spec = self.spec

        args = [
            self.define_from_variant('Z3_USE_LIB_GMP', 'gmp'),
            self.define_from_variant('Z3_BUILD_PYTHON_BINDINGS', 'python'),
            self.define_from_variant('Z3_INSTALL_PYTHON_BINDINGS', 'python')
        ]

        if spec.satisfies('+python'):
            args.append(
                self.define('CMAKE_INSTALL_PYTHON_PKG_DIR', join_path(
                    prefix.lib,
                    'python%s' % spec['python'].version.up_to(2),
                    'site-packages'))
            )

        return args
