# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlHtmlTagset(PerlPackage):
    """Data tables useful in parsing HTML"""

    homepage = "https://metacpan.org/pod/HTML::Tagset"
    url      = "http://search.cpan.org/CPAN/authors/id/P/PE/PETDANCE/HTML-Tagset-3.20.tar.gz"

    version('3.20', sha256='adb17dac9e36cd011f5243881c9739417fd102fce760f8de4e9be4c7131108e2')
