# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythonMapnik(PythonPackage):
    """
    Python bindings for mapnik
    """

    homepage = "https://github.com/mapnik/python-mapnik"
    url      = "https://github.com/mapnik/python-mapnik/archive/v3.0.16.tar.gz"

    version('3.0.16', sha256='643117752fa09668a1e26a360d13cd137329ae2013eb14ad92ab72fbc479fc70')
    version('3.0.13', sha256='ced684745e778c0cac0edba89c09c6f9b9f1db18fc12744ed4710a88b78a3389')

    depends_on('py-setuptools', type='build')
    depends_on('mapnik', type=('build', 'link', 'run'))
    depends_on('boost +python+thread')
    # py-pycairo is need by mapnik.printing
    depends_on('py-pycairo', type=('build', 'run'))

    # Package can't find boost_python without the following
    def setup_build_environment(self, env):
        # Inform the package that boost python library is of form
        # 'libboost_python27.so' as opposed to 'libboost_python.so'
        py_ver = str(self.spec['python'].version.up_to(2).joined)
        env.set('BOOST_PYTHON_LIB', 'boost_python' + py_ver)
