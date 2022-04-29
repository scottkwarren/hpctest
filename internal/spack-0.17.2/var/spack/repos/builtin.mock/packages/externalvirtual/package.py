# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Externalvirtual(Package):
    homepage = "http://somewhere.com"
    url      = "http://somewhere.com/stuff-1.0.tar.gz"

    version('1.0', '1234567890abcdef1234567890abcdef')
    version('2.0', '234567890abcdef1234567890abcdef1')
    version('2.1', '34567890abcdef1234567890abcdef12')
    version('2.2', '4567890abcdef1234567890abcdef123')

    provides('stuff', when='@1.0:')
