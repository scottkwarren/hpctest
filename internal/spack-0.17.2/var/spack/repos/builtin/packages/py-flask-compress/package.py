# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFlaskCompress(PythonPackage):
    """Flask-Compress allows you to easily compress your Flask application's
    responses with gzip."""

    homepage = "https://github.com/libwilliam/flask-compress"
    pypi = "Flask-Compress/Flask-Compress-1.4.0.tar.gz"

    version('1.4.0', sha256='468693f4ddd11ac6a41bca4eb5f94b071b763256d54136f77957cfee635badb3')

    depends_on('py-setuptools', type='build')
    depends_on('py-flask@0.9:', type=('build', 'run'))
