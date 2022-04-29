# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCinemasci(PythonPackage):
    """A set of python tools for reading, writing and viewing Cinema
    databases"""

    homepage = "https://github.com/cinemascience"
    pypi = "cinemasci/cinemasci-1.3.tar.gz"

    tags = ['e4s']

    maintainers = ['EthanS94']

    version('1.3', sha256='c024ca9791de9d78e5dad3fd11e8f87d8bc1afa5830f2697d7ec4116a5d23c20')

    variant('mpi', default=False, description='Enable MPI')

    depends_on('hdf5 ~mpi', when='~mpi')
    depends_on('hdf5 +mpi', when='+mpi')
    depends_on('pil', type=('build', 'run'))
    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-h5py~mpi', when='~mpi', type=('build', 'run'))
    depends_on('py-h5py+mpi', when='+mpi', type=('build', 'run'))
    depends_on('py-ipywidgets', type=('build', 'run'))
    depends_on('py-jupyterlab', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-setuptools', type=('build'))
