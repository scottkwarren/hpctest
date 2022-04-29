# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import subprocess

from spack import *


class Pvm(MakefilePackage):
    """PVM (Parallel Virtual Machine) is a software package that permits a
    heterogeneous collection of Unix and/or Windows computers hooked together
    by a network to be used as a single large parallel computer."""

    homepage = "https://www.csm.ornl.gov/pvm/pvm_home.html"
    url      = "https://www.netlib.org/pvm3/pvm3.4.6.tgz"

    version('3.4.6', sha256='482665e9bc975d826bcdacf1df1d42e43deda9585a2c430fd3b7b7ed08eada44')

    depends_on('m4', type='build')
    depends_on('libtirpc', type='link')

    variant('fpic', default=False,
            description='Enables -fPIC compilation flag on static libraries.')

    parallel = False

    @property
    def pvm_arch(self):
        """Returns the appropriate PVM_ARCH."""
        process = subprocess.Popen(['lib/pvmgetarch'], stdout=subprocess.PIPE)
        return process.communicate()[0].strip().decode()

    def edit(self, spec, prefix):
        # Before building PVM, you must set the environment
        # variable "PVM_ROOT" to the path where PVM resides
        env['PVM_ROOT'] = self.stage.source_path

    def patch(self):

        pvm_arch = self.pvm_arch

        if '+fpic' in self.spec:
            filter_file(
                '^SHAREDCFLAGS =',
                'SHAREDCFLAGS = -fPIC',
                join_path('conf', pvm_arch + '.def')
            )

    def setup_build_environment(self, env):
        tirpc = self.spec['libtirpc'].prefix
        env.prepend_path(
            'SPACK_INCLUDE_DIRS',
            tirpc.include.tirpc,
        )
        env.set('SPACK_LDLIBS', '-ltirpc')

    def install(self, spec, prefix):
        pvm_arch = self.pvm_arch

        install_tree(join_path('bin', pvm_arch), prefix.bin)
        install_tree('include', prefix.include)
        install_tree(join_path('lib', pvm_arch), prefix.lib)
        install_tree('man', prefix.man)

    def setup_run_environment(self, env):
        # Before running PVM, you must set the environment
        # variable "PVM_ROOT" to the path where PVM resides
        env.set('PVM_ROOT', self.prefix)
