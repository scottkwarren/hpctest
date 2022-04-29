# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyYoutubeDl(PythonPackage):
    """Command-line program to download videos from YouTube.com and other video
    sites."""

    homepage = "https://github.com/ytdl-org/youtube-dl"
    pypi = "youtube_dl/youtube_dl-2020.3.24.tar.gz"

    version('2020.3.24', sha256='4b03efe439f7cae26eba909821d1df00a9a4eb82741cb2e8b78fe29702bd4633')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('ffmpeg+openssl', type='run')
