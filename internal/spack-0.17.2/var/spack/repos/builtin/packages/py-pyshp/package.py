# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyshp(PythonPackage):
    """The Python Shapefile Library (pyshp) reads and writes ESRI Shapefiles in
    pure Python."""

    homepage = "https://github.com/GeospatialPython/pyshp"
    pypi = "pyshp/pyshp-1.2.12.tar.gz"

    version('2.1.0', sha256='e65c7f24d372b97d0920b864bbeb78322bb37b83f2606e2a2212631d5d51e5c0')
    version('1.2.12', sha256='8dcd65e0aa2aa2951527ddb7339ea6e69023543d8a20a73fc51e2829b9ed6179')

    depends_on('py-setuptools', type='build')
    depends_on('python@2.7:', type=('build', 'run'))
