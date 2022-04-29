# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAffyilm(RPackage):
    """Linear Model of background subtraction and the Langmuir isotherm

       affyILM is a preprocessing tool which estimates gene expression levels
       for Affymetrix Gene Chips. Input from physical chemistry is employed to
       first background subtract intensities before calculating concentrations
       on behalf of the Langmuir model."""

    homepage = "https://bioconductor.org/packages/affyILM"
    git      = "https://git.bioconductor.org/packages/affyILM.git"

    version('1.42.0', commit='b97b29786b866de38802ebbb995169be91e90942')
    version('1.36.0', commit='619ced931ba72860ce4cb41c841bbca1636a1132')
    version('1.34.0', commit='2c02ed2d8fa9a9585d41cf4db0b75d0a07ad8564')
    version('1.32.0', commit='860f2ddada80435d309ba334eff3fab503817755')
    version('1.30.0', commit='c07d91ae52a2a48f0a5f212c3ecf3243741bee13')
    version('1.28.0', commit='307bee3ebc599e0ea4a1d6fa8d5511ccf8bef7de')

    depends_on('r@2.10.0:', type=('build', 'run'))
    depends_on('r-gcrma', type=('build', 'run'))
    depends_on('r-affxparser@1.16.0:', type=('build', 'run'))
    depends_on('r-affy', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
