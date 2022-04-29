# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMime(RPackage):
    """Map Filenames to MIME Types

    Guesses the MIME type from a filename extension using the data derived
    from /etc/mime.types in UNIX-type systems."""

    homepage = "https://github.com/yihui/mime"
    cran     = "mime"

    version('0.11', sha256='215427a49f0d0b0e3ab38d419c515a35d57e3bc32535805306275d8b33f8eec0')
    version('0.9', sha256='2ccf97d2940a09539dc051c7a9a1aee90ef04b34e9bc6c0b64b4435fb3c2fa80')
    version('0.7', sha256='11083ee44c92569aadbb9baf60a2e079ab7a721c849b74d102694975cc8d778b')
    version('0.6', sha256='4775b605ab0117406bee7953c8af59eea8b35e67d1bd63f4007686a7097fc401')
    version('0.5', sha256='fcc72115afb0eb43237da872754464f37ae9ae097f332ec7984149b5e3a82145')
    version('0.4', sha256='d790c7e38371d03774a7d53f75aed3151835b1aebbb663b0fe828b221e6bac90')
