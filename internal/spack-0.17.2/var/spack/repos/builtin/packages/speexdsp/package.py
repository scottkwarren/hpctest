# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Speexdsp(AutotoolsPackage):
    """SpeexDSP is a patent-free, Open Source/Free Software DSP library."""

    homepage = "https://github.com/xiph/speexdsp"
    url      = "https://github.com/xiph/speexdsp/archive/SpeexDSP-1.2.0.tar.gz"

    version('1.2.0', sha256='d7032f607e8913c019b190c2bccc36ea73fc36718ee38b5cdfc4e4c0a04ce9a4')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    depends_on('fftw-api')

    patch('mkl.patch')

    def patch(self):
        filter_file('libspeexdsp_la_LIBADD = $(LIBM)',
                    'libspeexdsp_la_LIBADD = $(LIBM) $(FFT_LIBS)',
                    'libspeexdsp/Makefile.am',
                    string=True)

    def autoreconf(self, spec, prefix):
        autoreconf('--install', '--verbose', '--force')

    def configure_args(self):
        args = []

        if 'intel-mkl' in self.spec:
            # get the blas libs explicitly to avoid scalapack getting returned
            args.extend([
                '--with-fft=proprietary-intel-mkl',
                'CPPFLAGS={0}'.format(
                    self.spec['intel-mkl'].headers.cpp_flags),
                'LDFLAGS={0}'.format(self.spec['blas'].libs.ld_flags),
            ])
        elif 'fftw' in self.spec:
            args.append('--with-fft=gpl-fftw3')

        return args
