# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dracut(AutotoolsPackage):
    """dracut is used to create an initramfs image by copying tools and
    files from an installed system and combining it with the dracut
    framework."""

    homepage = "https://github.com/dracutdevs/dracut"
    url      = "https://github.com/dracutdevs/dracut/archive/050.tar.gz"

    version('050', sha256='f9dbf18597e5929221365964293212c8c9ffb7d84529c5a338c834ecab06e333')

    depends_on('kmod')
