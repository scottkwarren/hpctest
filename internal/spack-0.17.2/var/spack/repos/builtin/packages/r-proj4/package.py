# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RProj4(RPackage):
    """A simple interface to the PROJ.4 cartographic projections library

    A simple interface to lat/long projection and datum transformation of
    the PROJ.4 cartographic projections library. It allows transformation of
    geographic coordinates from one projection and/or datum to another."""

    homepage = "https://www.rforge.net/proj4/"
    url      = "https://cloud.r-project.org/src/contrib/proj4_1.0-8.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/proj4"

    version('1.0-10', sha256='5f396f172a17cfa9821a390f11ff7d3bff3c92ccf585572116dec459c621d1d0')
    version('1.0-8.1', sha256='a3a2a8f0014fd79fa34b5957440fd38299d8e97f1a802a61a068a6c6cda10a7e')

    depends_on('r@2.0.0:', type=('build', 'run'))
    depends_on('proj@4.4.6:5')
