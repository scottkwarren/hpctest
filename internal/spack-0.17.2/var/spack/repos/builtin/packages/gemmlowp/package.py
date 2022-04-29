# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gemmlowp(Package):
    """Google low-precision matrix multiplication library"""

    homepage = "https://github.com/google/gemmlowp"
    git      = "https://github.com/google/gemmlowp.git"

    version('a6f29d9ac', commit='a6f29d8ac48d63293f845f2253eccbf86bc28321')

    def install(self, spec, prefix):
        header_directories = ('eight_bit_int_gemm', 'fixedpoint',
                              'internal', 'meta', 'profiling', 'public')

        for directory in header_directories:
            install_tree(directory, join_path(prefix.include, directory))
