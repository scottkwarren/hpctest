# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
class WrongVariantInConflicts(Package):
    """This package has a wrong variant spelled in a conflict."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/b-1.0.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef')

    conflicts('+foo', when='@1.0')
