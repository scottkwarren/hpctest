# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class OpenalSoft(CMakePackage):
    """OpenAL provides capabilities for playing audio in a
    virtual 3D environment. Distance attenuation, doppler
    shift, and directional sound emitters are among the
    features handled by the API."""

    homepage = "https://openal-soft.org"
    url      = "https://openal-soft.org/openal-releases/openal-soft-1.21.1.tar.bz2"

    version('1.21.1', sha256='c8ad767e9a3230df66756a21cc8ebf218a9d47288f2514014832204e666af5d8')

    variant('alsa', default=False, description="ALSA support")

    depends_on('alsa-lib', when="+alsa")

    def cmake_args(self):
        args = [
            self.define_from_variant('ALSOFT_REQUIRE_ALSA', 'alsa')
        ]

        return args
