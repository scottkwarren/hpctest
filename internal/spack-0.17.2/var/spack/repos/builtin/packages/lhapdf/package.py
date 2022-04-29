# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lhapdf(AutotoolsPackage):
    """LHAPDF is a general purpose C++ interpolator,
       used for evaluating PDFs from discretised data files. """

    homepage = "https://lhapdf.hepforge.org/"
    url      = "https://lhapdf.hepforge.org/downloads/?f=LHAPDF-6.2.3.tar.gz"

    tags = ['hep']

    version('6.3.0', sha256='ed4d8772b7e6be26d1a7682a13c87338d67821847aa1640d78d67d2cef8b9b5d')
    version('6.2.3', sha256='d6e63addc56c57b6286dc43ffc56d901516f4779a93a0f1547e14b32cfd82dd1')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    depends_on('python',        type=('build', 'run'))
    depends_on('py-cython',     type='build')
    depends_on('py-setuptools', type='build')

    extends('python')

    def configure_args(self):
        args = ['FCFLAGS=-O3', 'CFLAGS=-O3', 'CXXFLAGS=-O3']
        return args
