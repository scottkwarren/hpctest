# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlObjectInsideout(PerlPackage):
    """Implements inside-out objects as anonymous scalar references
       that are blessed into a class with the scalar containing the
       ID for the object (usually a sequence number)."""

    homepage = "https://metacpan.org/pod/Object::InsideOut"
    url      = "https://cpan.metacpan.org/authors/id/J/JD/JDHEDDEN/Object-InsideOut-4.05.tar.gz"

    version('4.05', sha256='9dfd6ca2822724347e0eb6759d00709425814703ad5c66bdb6214579868bcac4')

    depends_on('perl-module-build', type='build')
    depends_on('perl-exception-class', type=('build', 'run'))
