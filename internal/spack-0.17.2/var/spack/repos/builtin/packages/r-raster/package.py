# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRaster(RPackage):
    """Geographic Data Analysis and Modeling

    Reading, writing, manipulating, analyzing and modeling of spatial data. The
    package implements basic and high-level functions for raster data and for
    vector data operations such as intersections. See the manual and tutorials
    on <https://rspatial.org/> to get started."""

    homepage = "https://cloud.r-project.org/package=raster"
    url      = "https://cloud.r-project.org/src/contrib/raster_2.5-8.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/raster"

    version('3.4-5', sha256='c6620d790b3aba1b64aec31325f726e63f26a14a1b48c1a0f9167a0b1a64e4a5')
    version('2.9-23', sha256='90aaec9e3b1e3e6015d9993ea7491e008f2f71990f8abb8610f979c4e28b38af')
    version('2.9-22', sha256='8107d95f1aa85cea801c8101c6aa391becfef4b5b915d9bc7a323531fee26128')
    version('2.5-8', sha256='47992abd783450513fbce3770298cc257030bf0eb77e42aa3a4b3924b16264cc')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r@3.5.0:', when='@3.4-5:', type=('build', 'run'))
    depends_on('r-sp@1.2-0:', type=('build', 'run'))
    depends_on('r-sp@1.4.1:', when='@3.4-5:', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
