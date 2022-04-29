# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRematch2(RPackage):
    """Wrappers on 'regexpr' and 'gregexpr' to return
       the match results in tidy data frames.
    """

    homepage = "https://cloud.r-project.org/package=rematch2"
    url      = "https://cloud.r-project.org/src/contrib/rematch2_2.1.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rematch2"

    version('2.1.2', sha256='fe9cbfe99dd7731a0a2a310900d999f80e7486775b67f3f8f388c30737faf7bb')
    version('2.1.1', sha256='d0423a418e8b46ac3a4819af7a7d19c39ca7c8c862c1e9a1c1294aa19152518f')
    version('2.1.0', sha256='78677071bd44b40e562df1da6f0c6bdeae44caf973f97ff8286b8c994db59f01')
    version('2.0.1', sha256='0612bb904334bd022ba6d1e69925b1e85f8e86b15ec65476777828776e89609a')

    depends_on('r-tibble')
