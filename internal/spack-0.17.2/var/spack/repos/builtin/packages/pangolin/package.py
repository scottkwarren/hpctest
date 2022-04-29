# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Pangolin(CMakePackage):
    """Pangolin is a lightweight portable rapid development library for
    managing OpenGL display / interaction and abstracting video input."""

    homepage = "https://github.com/stevenlovegrove/Pangolin"
    git      = "https://github.com/stevenlovegrove/Pangolin.git"

    version('master', branch='master')

    # Required dependencies
    depends_on('cmake@2.8.12:', type='build')
    depends_on('gl')
    depends_on('glew')
    depends_on('glu', type='link')

    # Optional dependencies
    depends_on('eigen')
