# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBackportsSslMatchHostname(PythonPackage):
    """The ssl.match_hostname() function from Python 3.5"""

    pypi = "backports.ssl_match_hostname/backports.ssl_match_hostname-3.5.0.1.tar.gz"

    py_namespace = 'backports'

    version('3.5.0.1', sha256='502ad98707319f4a51fa2ca1c677bd659008d27ded9f6380c79e8932e38dcdf2')
