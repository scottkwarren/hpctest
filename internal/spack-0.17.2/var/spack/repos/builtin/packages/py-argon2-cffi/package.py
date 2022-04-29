# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyArgon2Cffi(PythonPackage):
    """The secure Argon2 password hashing algorithm.."""

    homepage = "https://argon2-cffi.readthedocs.io/"
    pypi = "argon2-cffi/argon2-cffi-20.1.0.tar.gz"

    version('21.1.0', sha256='f710b61103d1a1f692ca3ecbd1373e28aa5e545ac625ba067ff2feca1b2bb870')
    version('20.1.0', sha256='d8029b2d3e4b4cea770e9e5a0104dd8fa185c1724a0f01528ae4826a6d25f97d')

    depends_on('python@2.7:2,3.5:', type=('build', 'run'))
    depends_on('python@3.5:', type=('build', 'run'), when='@21.1.0:')
    depends_on('py-setuptools', type='build')
    depends_on('py-cffi@1.0.0:', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'), when='@:20.1.0')
    depends_on('py-enum34', when='^python@:3.3', type=('build', 'run'))
