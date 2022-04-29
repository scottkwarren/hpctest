# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RLdheatmap(RPackage):
    """Graphical Display of Pairwise Linkage Disequilibria Between SNPs

    Produces a graphical display, as a heat map, of measures of pairwise
    linkage disequilibria between single nucleotide polymorphisms (SNPs). Users
    may optionally include the physical locations or genetic map distances of
    each SNP on the plot. The methods are described in  Shin et al. (2006)
    <doi:10.18637/jss.v016.c03>. Users should note that the imported package
    'snpStats' and the suggested packages  'rtracklayer', 'GenomicRanges',
    'GenomInfoDb' and 'IRanges' are all BioConductor packages
    <https://bioconductor.org>."""

    homepage = "https://sfustatgen.github.io/LDheatmap/"
    url      = "https://cloud.r-project.org/src/contrib/LDheatmap_0.99-7.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/LDheatmap"

    version('1.0-4', sha256='07eb385f19e6a195e8e4d75be0b47c57744eabbf14045e527f0c27e1183ae5ca')
    version('0.99-7', sha256='aca54c839a424506d8be7153bf03b32026aeefe7ed38f534e8e19708e34212e4')

    depends_on('r@2.14.0:', type=('build', 'run'))
    depends_on('r@4.0:', when='@1.0-4:', type=('build', 'run'))
    depends_on('r-genetics', type=('build', 'run'))
    depends_on('r-snpstats', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
