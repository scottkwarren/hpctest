# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlBioSearchioHmmer(PerlPackage):
    """BioPerl parser to HMMER output."""

    homepage = "https://github.com/bioperl/bio-searchio-hmmer"
    url      = "https://cpan.metacpan.org/authors/id/C/CJ/CJFIELDS/Bio-SearchIO-hmmer-1.7.3.tar.gz"

    version('1.7.3', sha256='686152f8ce7c611d27ee35ac002ecc309f6270e289a482993796a23bb5388246')

    depends_on('perl-bioperl', type=('build', 'run'))
    depends_on('perl-io-string', type=('build', 'run'))
