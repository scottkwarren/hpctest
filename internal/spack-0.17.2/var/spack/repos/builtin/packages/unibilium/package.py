# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Unibilium(Package):
    """A terminfo parsing library"""
    homepage = "https://github.com/mauke/unibilium"
    url      = "https://github.com/mauke/unibilium/archive/v2.0.0.tar.gz"

    version('2.0.0', sha256='78997d38d4c8177c60d3d0c1aa8c53fd0806eb21825b7b335b1768d7116bc1c1')
    version('1.2.0', sha256='623af1099515e673abfd3cae5f2fa808a09ca55dda1c65a7b5c9424eb304ead8')

    depends_on('libtool', type='build')

    def install(self, spec, prefix):
        make("PREFIX=" + prefix)
        make("install", "PREFIX=" + prefix)
