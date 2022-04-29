# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBiomartr(RPackage):
    """Perform large scale genomic data retrieval and functional annotation
    retrieval. This package aims to provide users with a standardized way to
    automate genome, proteome, 'RNA', coding sequence ('CDS'), 'GFF', and
    metagenome retrieval from 'NCBI RefSeq', 'NCBI Genbank', 'ENSEMBL',
    'ENSEMBLGENOMES', and 'UniProt' databases. Furthermore, an interface to the
    'BioMart' database (Smedley et al. (2009) <doi:10.1186/1471-2164-10-22>)
    allows users to retrieve functional annotation for genomic loci. In
    addition, users can download entire databases such as 'NCBI RefSeq' (Pruitt
    et al. (2007) <doi:10.1093/nar/gkl842>), 'NCBI nr', 'NCBI nt', 'NCBI
    Genbank' (Benson et al. (2013) <doi:10.1093/nar/gks1195>), etc. as well as
    'ENSEMBL' and 'ENSEMBLGENOMES' with only one command."""

    homepage = "https://docs.ropensci.org/biomartr"
    url      = "https://cloud.r-project.org/src/contrib/biomartr_0.9.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/biomartr"

    version('0.9.2', sha256='d88085696e9c5614828602254c33f2cdd3bbfeebc2f21a705eee3cb961097c89')

    depends_on('r-biomart', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
    depends_on('r-curl', type=('build', 'run'))
    depends_on('r-tibble', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-data-table@1.9.4:', type=('build', 'run'))
    depends_on('r-dplyr@0.3.0:', type=('build', 'run'))
    depends_on('r-readr@0.2.2:', type=('build', 'run'))
    depends_on('r-downloader@0.3:', type=('build', 'run'))
    depends_on('r-rcurl@1.95-4.5:', type=('build', 'run'))
    depends_on('r-xml@3.98-1.1:', type=('build', 'run'))
    depends_on('r-httr@0.6.1:', type=('build', 'run'))
    depends_on('r-stringr@0.6.2:', type=('build', 'run'))
    depends_on('r-purrr', type=('build', 'run'))
    depends_on('r-r-utils', type=('build', 'run'))
    depends_on('r-philentropy', type=('build', 'run'))
    depends_on('r-fs@1.3.1:', type=('build', 'run'))
