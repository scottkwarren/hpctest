# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAstropyHealpix(PythonPackage):
    """HEALPix (Hierarchical Equal Area isoLatitude Pixelisation) is
    an algorithm for pixellizing a sphere that is sometimes used in
    Astronomy to store data from all-sky surveys, but the general
    algorithm can apply to any field that has to deal with
    representing data on a sphere."""

    homepage = 'https://astropy-healpix.readthedocs.io/en/latest/'
    pypi = 'astropy-healpix/astropy-healpix-0.5.tar.gz'

    version('0.5', sha256='5ae15da796a840f221fb83e25de791e827b6921bc21a365d99bc1a59c7c0cdad')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-astropy@2.0:', type=('build', 'run'))
    depends_on('py-numpy@1.11:', type=('build', 'run'))
