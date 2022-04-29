# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
class DepWithVariantsIfDevelopRoot(Package):
    """Package that adds a dependency with many variants only at @develop"""
    homepage = "https://dev.null"

    version('1.0')

    depends_on('dep-with-variants-if-develop')
