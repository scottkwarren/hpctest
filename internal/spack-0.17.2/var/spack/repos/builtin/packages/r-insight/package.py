# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RInsight(RPackage):
    """Easy Access to Model Information for Various Model Objects

    A tool to provide an easy, intuitive and consistent access to information
    contained in various R models, like model formulas, model terms,
    information about random effects, data that was used to fit the model or
    data from response variables. 'insight' mainly revolves around two types of
    functions: Functions that find (the names of) information, starting with
    'find_', and functions that get the underlying data, starting with 'get_'.
    The package has a consistent syntax and works with many different model
    objects, where otherwise functions to access these information are
    missing."""

    homepage = "https://easystats.github.io/insight/"
    cran     = "insight"

    version('0.14.1', sha256='0e7761997a46ee33039cdeff1779dbc210de3644e4444c6e893e4ef2f12cc129')

    depends_on('r@3.4:', type=('build', 'run'))
