# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
#
import llnl.util.tty as tty

from spack import *


class Parsec(CMakePackage, CudaPackage):
    """PaRSEC: the Parallel Runtime Scheduler and Execution Controller

    PaRSEC is a runtime and a programming toolbox that support the design and
    parallel execution of micro-tasks on distributed, heterogeneous systems.
    """

    homepage    = "https://icl.utk.edu/dte"
    git         = "https://bitbucket.org/icldistcomp/parsec.git"
    url         = "https://bitbucket.org/icldistcomp/parsec/get/parsec-3.0.2012.tar.bz2"
    list_url    = "https://bitbucket.org/icldistcomp/parsec/downloads/?tab=tags"
    maintainers = ['abouteiller', 'bosilca', 'herault']
    tags = ['e4s']

    test_requires_compiler = True

    version('master', branch='master')
    version('3.0.2012', sha256='f565bcfffe106be8237b6aea3e83a5770607b7236606414b6f270244fa6ec3bc')
    version('1.1.0', sha256='d2928033c121000ae0a554f1e7f757c1f22274a8b74457ecd52744ae1f70b95a', url='https://bitbucket.org/icldistcomp/parsec/get/v1.1.0.tar.bz2')

    variant('build_type', default='RelWithDebInfo', description='CMake build type', values=('Debug', 'Release', 'RelWithDebInfo'))
    variant('shared', default=True, description='Build a shared library')
    variant('cuda', default=True, description='Build with CUDA')
    variant('profile', default=False, description='Generate profiling data')
    variant('debug_verbose', default=False, description='Debug version with verbose and paranoid (incurs performance overhead!)')
    conflicts('+debug_verbose build_type=Release', msg='You need to set build_type=Debug for +debug_verbose')
    conflicts('+debug_verbose build_type=RelWithDebInfo', msg='You need to set build_type=Debug for +debug_verbose')
    # TODO: Spack does not handle cross-compilation atm
    # variant('xcompile', default=False, description='Cross compile')

    depends_on('cmake@3.16:', type='build')
    depends_on('python', type='build')
    depends_on('flex', type='build')
    depends_on('bison', type='build')
    depends_on('hwloc')
    depends_on('mpi')
    depends_on('papi', when='+profile')
    depends_on('python', type=('build', 'run'), when='+profile')
    depends_on('py-cython', type=('build', 'run'), when='+profile')
    depends_on('py-pandas', type=('build', 'run'), when='+profile')
    depends_on('py-matplotlib', type=('build', 'run'),  when='+profile')
    depends_on('py-tables', type=('build', 'run'), when='+profile')

    def cmake_args(self):
        args = [
            self.define_from_variant('BUILD_SHARED_LIBS', 'shared'),
            self.define_from_variant('PARSEC_GPU_WITH_CUDA', 'cuda'),
            self.define_from_variant('PARSEC_PROF_TRACE', 'profile'),
            self.define_from_variant('PARSEC_DEBUG_HISTORY', 'debug_verbose'),
            self.define_from_variant('PARSEC_DEBUG_PARANOID', 'debug_verbose'),
        ]
        return args

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def check(self):
        """Run ctest after building binary."""
        with working_dir(self.build_directory):
            try:
                ctest('--output-on-failure', '-j1')
            except ProcessError:
                warn  = 'ctest tests failed.\n'
                warn += 'Please report this failure to:\n'
                warn += 'https://bitbucket.org/icldistcomp/parsec/issues'
                tty.msg(warn)

    def test(self):
        """Compile and run a user program with the installed library"""
        with working_dir(join_path(self.install_test_root,
                                   'contrib/build_with_parsec')):
            self.run_test('cmake',
                          options=['.'],
                          purpose='Check if CMake can find PaRSEC and its targets')
            self.run_test('make',
                          purpose='Check if tests can compile')
            self.run_test('./dtd_test_allreduce')
            self.run_test('./write_check')

    @run_after('install')
    def cache_test_sources(self):
        srcs = ['contrib/build_with_parsec']
        self.cache_extra_test_sources(srcs)
