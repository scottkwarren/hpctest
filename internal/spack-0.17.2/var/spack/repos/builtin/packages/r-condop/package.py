# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCondop(RPackage):
    """CONDOP: Condition-Dependent Operon Predictions.

    An implementation of the computational strategy for the comprehensive
    analysis of condition-dependent operon maps in prokaryotes proposed by
    Fortino et al. (2014) <doi:10.1186/1471-2105-15-145>. It uses RNA-seq
    transcriptome profiles to improve prokaryotic operon map inference."""

    homepage = "https://cloud.r-project.org/package=CONDOP"
    url      = "https://cloud.r-project.org/src/contrib/CONDOP_1.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/CONDOP"

    version('1.0', sha256='3a855880f5c6b33f949c7e6de53c8e014b4d72b7024a93878b344d3e52b5296a')

    depends_on('r-mclust', type=('build', 'run'))
    depends_on('r-earth', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-seqinr', type=('build', 'run'))
    depends_on('r-randomforest', type=('build', 'run'))
    depends_on('r-rminer', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-genomeinfodb', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
