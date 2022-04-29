# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libgtextutils(AutotoolsPackage):
    """Gordon's Text utils Library."""

    homepage = "https://github.com/agordon/libgtextutils"
    url      = "https://github.com/agordon/libgtextutils/releases/download/0.7/libgtextutils-0.7.tar.gz"

    patch('text_line_reader.patch')
    version('0.7', sha256='792e0ea3c96ffe3ad65617a104b7dc50684932bc96d2adab501c952fd65c3e4a')
