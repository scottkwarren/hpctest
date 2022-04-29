# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nextflow(Package):
    """Data-driven computational pipelines."""

    homepage = "https://www.nextflow.io"
    url      = "https://github.com/nextflow-io/nextflow/releases/download/v21.04.3/nextflow"

    maintainers = ['dialvarezs']

    version('21.04.3', sha256='80c7ecd94b55da8eb0e17040dbd0c43ee80e252cd999374e16c00d54d3d3abf3', expand=False)
    version('20.10.0', sha256='54f76c83cbabe8ec68d6a878dcf921e647284499f4ae917356e594d873cb78dd', expand=False)
    version('20.07.1', sha256='de4db5747a801af645d9b021c7b36f4a25c3ce1a8fda7705a5f37e8f9357443a', expand=False)
    version('20.04.1', sha256='b46833ad75b9b7db72668235b53d5c295a9ab02b50d36506bbbe53f383239bde', expand=False)
    version('20.01.0', sha256='fe1900284fd658c0781e6d8048839541afe5818d0b53f6ee8ae81f59d47ad662', expand=False)
    version('19.10.0', sha256='45497eb4bea62dd5477ebe75a6dabfd6905554c46321ca40aec6edfec61c59f4', expand=False)
    version('19.07.0', sha256='e6e7ba4770cd6230bd5410a6fd8c071d6c6dde7a7765880ecabc820b84d38fe5', expand=False)
    version('19.04.1', sha256='21318d8b64095a548f6baf0ef2811f33452e4f9f8a502a46a0aab7815ee34c69', expand=False)
    version('0.25.6', sha256='9498806596c96ba87396194fa6f1d7d1cdb739990f83e7e89d1d055366c5a943', expand=False, deprecated=True)
    version('0.24.1', sha256='0bfde5335b385e3cff99bf4aab619e583de5dc0849767240f675037a2e7c1d83', expand=False, deprecated=True)
    version('0.23.3', sha256='ffe1c314962ff97ebf47b0567883e152522acfbf6fd5800200b1a7a0ca2896d2', expand=False, deprecated=True)
    version('0.21.0', sha256='076089079479da0d91fe1ad7aad06816164ecbcf17f73c55e795b1db8462b28d', expand=False, deprecated=True)
    version('0.20.1', sha256='02635f3371f76a10e12f7366508c90bacf532ab7c23ae03c895317a150a39bd4', expand=False, deprecated=True)
    version('0.17.3', sha256='05563ee1474fbef22f65fa3080792dcb08d218dd1b1561c517ebff4346559dbe', expand=False, deprecated=True)

    depends_on('java')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install(self.stage.archive_file, join_path(prefix.bin, "nextflow"))
        set_executable(join_path(prefix.bin, "nextflow"))
