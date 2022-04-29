# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTidyselect(RPackage):
    """Select from a Set of Strings

    A backend for the selecting functions of the 'tidyverse'. It makes it easy
    to implement select-like functions in your own packages in a way that is
    consistent with other 'tidyverse' interfaces for selection."""

    homepage = "https://cloud.r-project.org/package=tidyselect"
    cran = "tidyselect"

    version('1.1.1', sha256='18eb6a6746196a81ce19ee6cbf1db0c33f494177b97e2419312ef25a00ae486b')
    version('1.1.0', sha256='e635ed381fb53f7a53c3fa36bb33e134a3273d272367de2a8d909c821be93893')
    version('0.2.5', sha256='5ce2e86230fa35cfc09aa71dcdd6e05e1554a5739c863ca354d241bfccb86c74')
    version('0.2.4', sha256='5cb30e56ad5c1ac59786969edc8d542a7a1735a129a474f585a141aefe6a2295')
    version('0.2.3', sha256='0c193abc8251a60e1d2a32a99c77651c336bc185e3c2a72e5f8781813d181c2c')

    depends_on('r@3.1:', type=('build', 'run'))
    depends_on('r@3.2:', when='@1.1.0:', type=('build', 'run'))
    depends_on('r-ellipsis', when='@1.1.0:', type=('build', 'run'))
    depends_on('r-glue@1.3.0:', type=('build', 'run'))
    depends_on('r-purrr', type=('build', 'run'))
    depends_on('r-purrr@0.3.2:', when='@1.1.0:', type=('build', 'run'))
    depends_on('r-rlang@0.2.2:', type=('build', 'run'))
    depends_on('r-rlang@0.4.6:', when='@1.1.0:', type=('build', 'run'))
    depends_on('r-vctrs@0.2.2:', when='@1.1.0:', type=('build', 'run'))
    depends_on('r-vctrs@0.3.0:', when='@1.1.1:', type=('build', 'run'))

    depends_on('r-rcpp@0.12.0:', when='@:0.2.5', type=('build', 'run'))
