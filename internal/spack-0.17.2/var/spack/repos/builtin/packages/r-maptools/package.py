# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMaptools(RPackage):
    """Tools for Handling Spatial Objects

    Set of tools for manipulating and reading geographic data, in particular
    ESRI shapefiles; C code used from shapelib. It includes binary access to
    GSHHG shoreline files. The package also provides interface wrappers for
    exchanging spatial objects with packages such as PBSmapping, spatstat,
    maps, RArcInfo, Stata tmap, WinBUGS, Mondrian, and others."""

    homepage = "https://r-forge.r-project.org/projects/maptools/"
    url      = "https://cloud.r-project.org/src/contrib/maptools_0.8-39.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/maptools"

    version('1.0-2', sha256='daac6da5817cf0cff17b9e7d4a7cdc7c329574249bd9b1bafdb6c9431e1fee49')
    version('0.9-5', sha256='5d9511f09fb49d57a51f28495b02239800596a4fcfad7b03ee1074d793657bdd')
    version('0.9-4', sha256='930875f598a516f0f9049fa2fae7391bc9bdf7e3e5db696059ab4ec2fc9ba39c')
    version('0.8-39', sha256='4b81e313e45dbb75e0fbb180b02985d1c34aaa5669e483283b632788e6a67dd2')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-sp@1.0-11:', type=('build', 'run'))
    depends_on('r-foreign@0.8:', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
