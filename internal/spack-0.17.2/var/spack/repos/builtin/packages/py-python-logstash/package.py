# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythonLogstash(PythonPackage):
    """Python logging handler for Logstash."""

    homepage = "https://github.com/vklochan/python-logstash"
    pypi = "python-logstash/python-logstash-0.4.6.tar.gz"

    version('0.4.6', sha256='10943e5df83f592b4d61b63ad1afff855ccc8c9467f78718f0a59809ba1fe68c')
