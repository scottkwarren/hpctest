# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ExonerateGff3(AutotoolsPackage):
    """This is an exonerate fork with added gff3 support.
       Original website with user guides:
       http://www.ebi.ac.uk/~guy/exonerate/"""

    homepage = "https://github.com/hotdogee/exonerate-gff3/"
    url      = "https://github.com/hotdogee/exonerate-gff3/archive/2.3.0.tar.gz"

    version('2.3.0', sha256='eeab7ea8bc815fc4a37d4c3b89c625167a9a60a4a833b5cc96e32dc313eafd1f')

    depends_on('glib')

    # parallel builds fail occasionally
    parallel = False
