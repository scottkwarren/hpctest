# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Efivar(MakefilePackage):
    """Tools and libraries to work with EFI variables"""

    homepage = "https://github.com/rhboot/efivar"
    url      = "https://github.com/rhboot/efivar/archive/37.tar.gz"

    version('37', sha256='74c52b4f479120fb6639e753e71163ba3f557a7a67c0be225593f9f05b253f36')
    version('36', sha256='24ed0cafbaf6d913e8f60e5da3cbbac1a1578e16cf5c95b21f2eb6753c13173f')
    version('35', sha256='747bc4d97b4bd74979e5356c44a172534a8a07184f130349fd201742e683d292')

    def install(self, spec, prefix):
        make('PREFIX={0}'.format(prefix), 'install')
