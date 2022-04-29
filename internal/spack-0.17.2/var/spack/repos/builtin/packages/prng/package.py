# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Prng(AutotoolsPackage):
    """Pseudo-Random Number Generator library."""

    homepage = "https://statmath.wu.ac.at/prng/"
    url      = "https://statmath.wu.ac.at/prng/prng-3.0.2.tar.gz"

    version('3.0.2', sha256='8299182b97c24b7891d74590a8a8438641a6c681ce34d6c3f7bc98a0649da48b')

    depends_on('automake', type='build')
    depends_on('autoconf', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')

    patch('prng-3.0.2-shared.patch', when="@3.0.2")
    patch('prng-3.0.2-fix-c99-inline-semantics.patch', when="@3.0.2")

    # Force the autoreconf step
    force_autoreconf = True
