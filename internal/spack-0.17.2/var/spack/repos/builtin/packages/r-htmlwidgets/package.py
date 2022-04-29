# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RHtmlwidgets(RPackage):
    """HTML Widgets for R

    A framework for creating HTML widgets that render in various contexts
    including the R console, 'R Markdown' documents, and 'Shiny' web
    applications."""

    homepage = "https://cloud.r-project.org/package=htmlwidgets"
    url      = "https://cloud.r-project.org/src/contrib/htmlwidgets_0.9.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/htmlwidgets"

    version('1.5.3', sha256='01a5833182cc224bd100be2815e57e67b524de9f2bb1542787b6e3d1303f0f29')
    version('1.3', sha256='f1e4ffabc29e6cfe857f627da095be3cfcbe0e1f02ae75e572f10b4a026c5a12')
    version('0.9', sha256='1154b541ccd868e41d3cf0d7f188f7275ec99f61fe2c7de21c8a05edb19b985e')
    version('0.8', sha256='9232b78727c1ecd006cd8e607ef76417d795f011b0e4a7535e6d673228bfc3b5')
    version('0.6', sha256='9c227f93ada71526d6e195e39a8efef41255af5567e39db3a6417ea9fed192ea')

    depends_on('r-htmltools@0.3:', type=('build', 'run'))
    depends_on('r-jsonlite@0.9.16:', type=('build', 'run'))
    depends_on('r-yaml', type=('build', 'run'))
