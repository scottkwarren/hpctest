# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import tempfile

from spack import *


class PyTensorflowEstimator(Package):
    """TensorFlow Estimator is a high-level TensorFlow API that greatly
    simplifies machine learning programming."""

    homepage = "https://github.com/tensorflow/estimator"
    url      = "https://github.com/tensorflow/estimator/archive/v2.2.0.tar.gz"

    maintainers = ['aweits']

    version('2.4.0', sha256='e6ea12014c3d8c89a81ace95f8f8b7c39ffcd3e4e4626709e4aee0010eefd962')
    version('2.3.0', sha256='75403e7de7e8ec30ec0781ede56ed84cbe5e90daad64a9c242cd489c8fe63a17')
    version('2.2.0', sha256='2d68cb6e6442e7dcbfa2e092aa25bdcb0eda420536a829b85d732854a4c85d46')
    version('2.1', sha256='1d74c8181b981748976fa33ad97d3434c3cf2b7e29a0b00861365fe8329dbc4e')
    version('2.0.0', sha256='6f4bdf1ab219e1f1cba25d2af097dc820f56479f12a839853d97422fe4d8b465')
    version('1.13.0', sha256='a787b150ff436636df723e507019c72a5d6486cfe506886279d380166953f12f')

    extends('python')

    depends_on('py-tensorflow@2.4.0:2.4', type=('build', 'run'), when='@2.4.0')
    depends_on('py-tensorflow@2.3.0:2.3', type=('build', 'run'), when='@2.3.0')
    depends_on('py-tensorflow@2.2.0:2.2', type=('build', 'run'), when='@2.2.0')
    depends_on('py-tensorflow@2.1.0:2.1', type=('build', 'run'), when='@2.1')
    depends_on('py-tensorflow@2.0.0:2.0', type=('build', 'run'), when='@2.0.0')
    depends_on('py-tensorflow@1.13.1', type=('build', 'run'), when='@1.13.0')

    depends_on('bazel@0.19.0:', type='build')
    depends_on('py-funcsigs@1.0.2:', type=('build', 'run'))

    def install(self, spec, prefix):
        self.tmp_path = tempfile.mkdtemp(dir='/tmp', prefix='spack')
        env['TEST_TMPDIR'] = self.tmp_path
        env['HOME'] = self.tmp_path

        args = [
            # Don't allow user or system .bazelrc to override build settings
            '--nohome_rc',
            '--nosystem_rc',
            # Bazel does not work properly on NFS, switch to /tmp
            '--output_user_root=' + self.tmp_path,
            'build',
            # Spack logs don't handle colored output well
            '--color=no',
            '--jobs={0}'.format(make_jobs),
            # Enable verbose output for failures
            '--verbose_failures',
            # Show (formatted) subcommands being executed
            '--subcommands=pretty_print',
            '--spawn_strategy=local',
            # Ask bazel to explain what it's up to
            # Needs a filename as argument
            '--explain=explainlogfile.txt',
            # Increase verbosity of explanation,
            '--verbose_explanations',
            # bazel uses system PYTHONPATH instead of spack paths
            '--action_env', 'PYTHONPATH={0}'.format(env['PYTHONPATH']),
            '//tensorflow_estimator/tools/pip_package:build_pip_package',
        ]

        bazel(*args)

        build_pip_package = Executable(join_path(
            'bazel-bin/tensorflow_estimator/tools',
            'pip_package/build_pip_package'))
        buildpath = join_path(self.stage.source_path, 'spack-build')
        build_pip_package('--src', buildpath)
        with working_dir(buildpath):
            setup_py('install', '--prefix={0}'.format(prefix),
                     '--single-version-externally-managed', '--root=/')
        remove_linked_tree(self.tmp_path)
