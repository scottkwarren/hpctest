# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Readfq(Package):
    """Readfq is a collection of routines for parsing the FASTA/FASTQ format.
    It seamlessly parses both FASTA and multi-line FASTQ with a simple
    interface."""

    homepage = "https://github.com/lh3/readfq"
    git      = "https://github.com/lh3/readfq.git"

    version('2013.04.10', commit='4fb766095d8f459e0f8025be70f9173673905d12')

    def install(self, spec, prefix):
        install_tree('.', prefix.bin)
