# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyCatalogue(PythonPackage):
    """catalogue: Super lightweight function registries for your library."""

    homepage = "https://github.com/explosion/catalogue"
    pypi = "catalogue/catalogue-2.0.0.tar.gz"

    version('2.0.0', sha256='34f8416ec5e7ed08e55c10414416e67c3f4d66edf83bc67320c3290775293816')
    version('1.0.0', sha256='d74d1d856c6b36a37bf14aa6dbbc27d0582667b7ab979a6108e61a575e8723f5')

    depends_on('python@3.6:', when='@2:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-importlib-metadata@0.20:', when='^python@:3.7', type=('build', 'run'))
