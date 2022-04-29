# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Externaltool(Package):
    homepage = "http://somewhere.com"
    url      = "http://somewhere.com/tool-1.0.tar.gz"

    version('1.0', '1234567890abcdef1234567890abcdef')
    version('0.9', '1234567890abcdef1234567890abcdef')
    version('0.8.1', '1234567890abcdef1234567890abcdef')

    depends_on('externalprereq')
