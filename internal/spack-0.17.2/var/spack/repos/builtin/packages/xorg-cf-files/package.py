# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class XorgCfFiles(AutotoolsPackage, XorgPackage):
    """The xorg-cf-files package contains the data files for the imake utility,
    defining the known settings for a wide variety of platforms (many of which
    have not been verified or tested in over a decade), and for many of the
    libraries formerly delivered in the X.Org monolithic releases."""

    homepage = "https://cgit.freedesktop.org/xorg/util/cf"
    xorg_mirror_path = "util/xorg-cf-files-1.0.6.tar.gz"

    version('1.0.6', sha256='6d56094e5d1a6c7d7a9576ac3a0fc2c042344509ea900d59f4b23df668b96c7a')

    depends_on('pkgconfig', type='build')
