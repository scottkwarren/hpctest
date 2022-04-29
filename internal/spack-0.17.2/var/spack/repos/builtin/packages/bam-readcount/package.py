# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class BamReadcount(CMakePackage):
    """Bam-readcount generates metrics at single nucleotide positions."""

    homepage = "https://github.com/genome/bam-readcount"
    url      = "https://github.com/genome/bam-readcount/archive/v0.8.0.tar.gz"

    version('0.8.0', sha256='4f4dd558e3c6bfb24d6a57ec441568f7524be6639b24f13ea6f2bb350c7ea65f')
