# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Maintainers2(Package):
    """A second package with a maintainers field."""

    homepage = "http://www.example.com"
    url      = "http://www.example.com/maintainers2-1.0.tar.gz"

    maintainers = ['user2', 'user3']

    version('1.0', '0123456789abcdef0123456789abcdef')
