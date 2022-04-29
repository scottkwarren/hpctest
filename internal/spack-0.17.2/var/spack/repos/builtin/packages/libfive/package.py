# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libfive(CMakePackage):
    """libfive is a software library and set of tools for solid modeling."""

    homepage = "https://libfive.com"
    git      = "https://github.com/libfive/libfive.git"

    # https://libfive.com/download/ recommends working from the master branch
    # and currently, all tags are from 2017:
    version('master', branch='master')

    depends_on('pkgconfig', type='build')
    depends_on('cmake@3.12:', type='build')
    depends_on('boost@1.65:')
    depends_on('eigen@3.3.0:')
    depends_on('libpng')
    depends_on('python@3:',         when='+python', type=('link', 'run'))
    depends_on('guile@2.2.1:',      when='+guile')
    # In case build of future git master fails, check raising the minimum Qt version
    depends_on('qt@5.15.2:+opengl', when='+qt')

    variant('qt',     default=True, description='Enable Studio UI(with Guile or Python)')
    variant('guile',  default=True, description='Enable Guile support for Studio UI')
    variant('python', default=True, description='Enable Python support for Studio UI')

    variant('packed_opcodes', default=False,
            description='packed opcodes breaks compatibility with saved f-reps!')

    def cmake_args(self):
        if self.spec.satisfies('+qt~guile~python'):
            raise InstallError('The Qt-based Studio UI (+qt) needs +guile or +python!')

        return [self.define_from_variant('BUILD_STUDIO_APP',       'qt'),
                self.define_from_variant('BUILD_GUILE_BINDINGS',   'guile'),
                self.define_from_variant('BUILD_PYTHON_BINDINGS',  'python'),
                self.define_from_variant('LIBFIVE_PACKED_OPCODES', 'packed_opcodes')]
