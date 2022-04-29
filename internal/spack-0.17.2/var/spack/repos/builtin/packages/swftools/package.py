# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Swftools(AutotoolsPackage):
    """SWFTools is a collection of utilities for working with Adobe Flash files
    (SWF files). The tool collection includes programs for reading SWF files,
    combining them, and creating them from other content (like images, sound
    files, videos or sourcecode). SWFTools is released under the GPL.
    """

    homepage = "http://swftools.org"
    url      = "http://swftools.org/swftools-0.9.2.tar.gz"

    version('0.9.2', sha256='bf6891bfc6bf535a1a99a485478f7896ebacbe3bbf545ba551298080a26f01f1')

    patch('configure.patch')
    patch('swfs_Makefile.in.patch')
    patch('https://aur.archlinux.org/cgit/aur.git/plain/giflib-5.1.patch?h=swftools',
          sha256='6a995dfd674c5954f5b967e3d45d6845a186872fcaa4223d725902fd4d679f1b',
          level=0)

    depends_on('giflib')
    depends_on('lame')
    depends_on('poppler')
    depends_on('freetype')
    depends_on('jpeg')
    depends_on('fftw')
