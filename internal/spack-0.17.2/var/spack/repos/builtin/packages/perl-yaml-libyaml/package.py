# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlYamlLibyaml(PerlPackage):
    """Perl YAML Serialization using XS and libyaml  """

    homepage = "https://metacpan.org/pod/YAML::LibYAML"
    url      = "http://search.cpan.org/CPAN/authors/id/T/TI/TINITA/YAML-LibYAML-0.67.tar.gz"

    version('0.67', sha256='e65a22abc912a46a10abddf3b88d806757f44f164ab3167c8f0ff6aa30648187')
