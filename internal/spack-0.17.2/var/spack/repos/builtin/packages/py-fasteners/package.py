# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFasteners(PythonPackage):
    """A python package that provides useful locks."""

    homepage = "https://github.com/harlowja/fasteners"
    pypi = "fasteners/fasteners-0.14.1.tar.gz"

    version('0.16.3', sha256='b1ab4e5adfbc28681ce44b3024421c4f567e705cc3963c732bf1cba3348307de')
    version('0.14.1', sha256='427c76773fe036ddfa41e57d89086ea03111bbac57c55fc55f3006d027107e18')

    depends_on('py-setuptools',     type='build')
    depends_on('py-monotonic@0.1:', type=('build', 'run'), when='@0.14.1')
    depends_on('py-monotonic@0.1:', type=('build', 'run'), when='@0.16.3: ^python@:3.3')
    depends_on('py-six',            type=('build', 'run'))
