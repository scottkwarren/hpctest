# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyColorful(PythonPackage):
    """Terminal string styling done right, in Python."""

    homepage = "https://github.com/timofurrer/colorful"
    pypi = "colorful/colorful-0.5.4.tar.gz"

    version('0.5.4', sha256='86848ad4e2eda60cd2519d8698945d22f6f6551e23e95f3f14dfbb60997807ea')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
