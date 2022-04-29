# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Vardictjava(Package):
    """VarDictJava is a variant discovery program written in Java.
    It is a partial Java port of VarDict variant caller."""

    homepage = "https://github.com/AstraZeneca-NGS/VarDictJava"
    url      = "https://github.com/AstraZeneca-NGS/VarDictJava/releases/download/v1.5.1/VarDict-1.5.1.tar"

    version('1.5.1', sha256='f1d710d238e8ab41b02a99fa8698baeee8c8668635a847b826913dd03a9176b9')

    depends_on('java@8:', type='run')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('bin/VarDict', prefix.bin)

        mkdirp(prefix.lib)
        install('lib/*.jar', prefix.lib)
