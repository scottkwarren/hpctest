# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RColourpicker(RPackage):
    """A Colour Picker Tool for Shiny and for Selecting Colours in Plots:

    A colour picker that can be used as an input in 'Shiny' apps or Rmarkdown
    documents. The colour picker supports alpha opacity, custom colour
    palettes, and many more options. A Plot Colour Helper tool is available as
    an 'RStudio' Addin, which helps you pick colours to use in your plots. A
    more generic Colour Picker 'RStudio' Addin is also provided to let you
    select colours to use in your R code."""

    homepage = "https://github.com/daattali/colourpicker"
    cran     = "colourpicker"

    version('1.1.0', sha256='2dfbb6262d187d3b17357ff9c22670ced3621feda5b2a2a500558478e4d551e2')

    depends_on('r@3.1.0:', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-htmltools', type=('build', 'run'))
    depends_on('r-htmlwidgets@0.7:', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-miniui@0.1.1:', type=('build', 'run'))
    depends_on('r-shiny@0.11.1:', type=('build', 'run'))
    depends_on('r-shinyjs@2.0.0:', type=('build', 'run'))
