# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRcolorbrewer(RPackage):
    """Provides color schemes for maps (and other graphics) designed by Cynthia
    Brewer as described at https://colorbrewer2.org/"""

    homepage = "https://colorbrewer2.org"
    url      = "https://cloud.r-project.org/src/contrib/RColorBrewer_1.1-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/RColorBrewer"

    version('1.1-2', sha256='f3e9781e84e114b7a88eb099825936cc5ae7276bbba5af94d35adb1b3ea2ccdd')

    depends_on('r@2.0.0:', type=('build', 'run'))
