# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAssertiveDataUk(RPackage):
    """assertive.data.uk: Assertions to Check Properties of Strings

    A set of predicates and assertions for checking the
    properties of UK-specific complex data types. This is
    mainly for use by other package developers who want to
    include run-time testing features in their own packages.
    End-users will usually want to use assertive directly."""

    homepage = "https://bitbucket.org/richierocks/assertive.data.uk"
    url      = "https://cloud.r-project.org/src/contrib/assertive.data.uk_0.0-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/assertive.data.uk"

    version('0.0-2', sha256='ab48dab6977e8f43d6fffb33228d158865f68dde7026d123c693d77339dcf2bb')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-assertive-base@0.0-2:', type=('build', 'run'))
    depends_on('r-assertive-strings', type=('build', 'run'))
