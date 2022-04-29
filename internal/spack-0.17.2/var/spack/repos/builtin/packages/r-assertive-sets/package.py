# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAssertiveSets(RPackage):
    """assertive.sets: Assertions to Check Properties of Sets

    A set of predicates and assertions for checking the
    properties of sets. This is mainly for use by other package
    developers who want to include run-time testing features in
    their own packages. End-users will usually want to use
    assertive directly."""

    homepage = "https://bitbucket.org/richierocks/assertive.sets"
    url      = "https://cloud.r-project.org/src/contrib/assertive.sets_0.0-3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/assertive.sets"

    version('0.0-3', sha256='876975a16ed911ea1ad12da284111c6eada6abfc0118585033abc0edb5801bb3')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-assertive-base@0.0-7:', type=('build', 'run'))
