# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
class DepWithVariants(Package):
    """Package that has a variant which adds a dependency forced to
    use non default values.
    """
    homepage = "https://dev.null"

    version('1.0')

    variant('foo', default=False, description='nope')
    variant('bar', default=False, description='nope')
    variant('baz', default=False, description='nope')
