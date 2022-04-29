# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class FluxSched(AutotoolsPackage):
    """ A scheduler for flux-core (pre-alpha) """

    homepage = "https://github.com/flux-framework/flux-sched"
    url      = "https://github.com/flux-framework/flux-sched/releases/download/v0.5.0/flux-sched-0.5.0.tar.gz"
    git      = "https://github.com/flux-framework/flux-sched.git"
    tags     = ['radiuss', 'e4s']

    maintainers = ['grondo']

    version('master', branch='master')
    version('0.19.0', sha256='8dffa8eaec95a81286f621639ef851c52dc4c562d365971233bbd91100c31ed2')
    version('0.18.0', sha256='a4d8a6444fdb7b857b26f47fdea57992b486c9522f4ff92d5a6f547d95b586ae')
    version('0.17.0', sha256='5acfcb757e2294a92eaa91be58ba9b42736b88b42d2937de4a78f4642b1c4933')
    version('0.16.0', sha256='08313976161c141b9b34e2d44d5a08d1b11302e22d60aeaf878eef84d4bd2884')
    version('0.15.0', sha256='ff24d26997f91af415f98734b8117291f5a5001e86dac865b56b3d72980c80c8')
    version('0.14.0', sha256='2808f42032b917823d69cd26103c9238694416e2f30c6d39c11c670927ed232a')
    version('0.13.0', sha256='ba17fc0451239fe31a1524b6a270741873f59a5057514d2524fd3e9215c47a82')
    version('0.12.0', sha256='b41ecaebba254abfb5a7995fd9100bd45a59d4ad0a79bdca8b3db02785d97b1d')
    version('0.11.0', sha256='6a0e3c0678f85da8724e5399b02be9686311c835617f6036235ef54b489cc336')
    version('0.10.0', sha256='5944927774709b5f52ddf64a0e825d9b0f24c9dea890b5504b87a8576d217cf6')
    version('0.9.0',  sha256='0e1eb408a937c2843bdaaed915d4d7e2ea763b98c31e7b849a96a74758d66a21')
    version('0.8.0', sha256='45bc3cefb453d19c0cb289f03692fba600a39045846568d258e4b896ca19ca0d')

    # Avoid the infinite symlink issue
    # This workaround is documented in PR #3543
    build_directory = 'spack-build'

    variant('cuda', default=False, description='Build dependencies with support for CUDA')

    depends_on("boost+graph@1.53.0,1.59.0:")
    depends_on("py-pyyaml")
    depends_on("libedit")
    depends_on("libxml2@2.9.1:")
    depends_on("yaml-cpp")
    depends_on("uuid")
    depends_on("pkgconfig")

    depends_on("flux-core", type=('build', 'link', 'run'))
    depends_on("flux-core+cuda", when='+cuda', type=('build', 'run', 'link'))
    depends_on("flux-core@0.16.0:0.16", when='@0.8.0', type=('build', 'run', 'link'))
    depends_on("flux-core@0.22.0", when='@0.14.0', type=('build', 'run', 'link'))
    depends_on("flux-core@0.23.0:0.25", when='@0.15.0', type=('build', 'run', 'link'))
    depends_on("flux-core@0.26.0:", when='@0.16.0', type=('build', 'run', 'link'))
    depends_on("flux-core@0.28.0:", when='@0.17.0', type=('build', 'run', 'link'))
    depends_on("flux-core@0.29.0:", when='@0.18.0', type=('build', 'run', 'link'))
    depends_on("flux-core@0.30.0:", when='@0.19.0', type=('build', 'run', 'link'))
    depends_on("flux-core@master", when='@master', type=('build', 'run', 'link'))

    # Need autotools when building on master:
    depends_on("autoconf", type='build', when='@master')
    depends_on("automake", type='build', when='@master')
    depends_on("libtool", type='build', when='@master')

    def url_for_version(self, version):
        '''
        Flux uses a fork of ZeroMQ's Collective Code Construction Contract
        (https://github.com/flux-framework/rfc/blob/master/spec_1.adoc).
        This model requires a repository fork for every stable release that has
        patch releases.  For example, 0.8.0 and 0.9.0 are both tags within the
        main repository, but 0.8.1 and 0.9.5 would be releases on the v0.8 and
        v0.9 forks, respectively.

        Rather than provide an explicit URL for each patch release, make Spack
        aware of this repo structure.
        '''
        if version[-1] == 0:
            url = "https://github.com/flux-framework/flux-sched/releases/download/v{0}/flux-sched-{0}.tar.gz"
        else:
            url = "https://github.com/flux-framework/flux-sched-v{1}/releases/download/v{0}/flux-sched-{0}.tar.gz"
        return url.format(version.up_to(3), version.up_to(2))

    def setup(self):
        pass

    @when('@master')
    def setup(self):
        with working_dir(self.stage.source_path):
            # Allow git-describe to get last tag so flux-version works:
            git = which('git')
            git('fetch', '--unshallow')
            git("config", "remote.origin.fetch",
                "+refs/heads/*:refs/remotes/origin/*")
            git('fetch', 'origin')

    def autoreconf(self, spec, prefix):
        self.setup()
        if os.path.exists(self.configure_abs_path):
            return
        # make sure configure doesn't get confused by the staging symlink
        with working_dir(self.configure_directory):
            # Bootstrap with autotools
            bash = which('bash')
            bash('./autogen.sh')

    @when('@:0.19')
    def patch(self):
        """Fix build with clang@13 and gcc@11"""
        filter_file('NULL', 'nullptr', 'resource/schema/sched_data.hpp')
        filter_file('size_t', 'std::size_t', 'resource/planner/planner.h')

    def configure_args(self):
        args = []
        if self.spec.satisfies('@0.9.0:'):
            args.append('CXXFLAGS=-Wno-uninitialized')
        if self.spec.satisfies('%clang@12:'):
            args.append('CXXFLAGS=-Wno-defaulted-function-deleted')
        # flux-sched's ax_boost is sometimes weird about non-system locations
        # explicitly setting the path guarantees success
        args.append('--with-boost={0}'.format(self.spec['boost'].prefix))
        return args

    @property
    def lua_version(self):
        return self.spec['lua'].version.up_to(2)

    @property
    def lua_share_dir(self):
        return os.path.join('share', 'lua', str(self.lua_version))

    @property
    def lua_lib_dir(self):
        return os.path.join('lib', 'lua', str(self.lua_version))

    def setup_run_environment(self, env):
        env.prepend_path(
            'LUA_PATH',
            os.path.join(self.spec.prefix, self.lua_share_dir, '?.lua'),
            separator=';')
        env.prepend_path(
            'LUA_CPATH',
            os.path.join(self.spec.prefix, self.lua_lib_dir, '?.so'),
            separator=';')

        env.prepend_path('FLUX_MODULE_PATH', self.prefix.lib.flux.modules)
        env.prepend_path('FLUX_MODULE_PATH',
                         self.prefix.lib.flux.modules.sched)
        env.prepend_path('FLUX_EXEC_PATH', self.prefix.libexec.flux.cmd)
        env.prepend_path('FLUX_RC_EXTRA', self.prefix.etc.flux)
