# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythonsollya(PythonPackage):
    """Python wrapper for the Sollya library"""

    homepage = "Python wrapper for the Sollya library"
    url      = "https://gitlab.com/metalibm-dev/pythonsollya/-/archive/release-0.4.0-alpha0/pythonsollya-release-0.4.0-alpha0.tar.gz"

    version('0.4.0-alpha0', sha256='faac899744c92b1d20980cadef309cd5610d79722322e97940ff142c207c41b5')
    version('0.3.0', url='https://gitlab.com/metalibm-dev/pythonsollya/-/archive/0.3/pythonsollya-0.3.tar.gz',
            sha256='cdccd0c5549247ad7498546095544d8d01e78bcb4a3e55c32d6daea6b845b6b9', preferred=True)

    depends_on('py-cython', type='build')
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('libffi', type='build')
    depends_on('sollya', type=('build', 'link'))
    depends_on('py-bigfloat', type=('build', 'run'))
    depends_on('mpfi', type=('build', 'link'))
