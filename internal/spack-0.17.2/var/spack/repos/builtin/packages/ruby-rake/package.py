# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class RubyRake(RubyPackage):
    """Rake is a Make-like program implemented in Ruby."""

    homepage = "https://github.com/ruby/rake"
    url      = "https://github.com/ruby/rake/archive/v13.0.1.tar.gz"

    version('13.0.1', sha256='d865329b5e0c38bd9d11ce70bd1ad6e0d5676c4eee74fd818671c55ec49d92fd')

    depends_on('ruby@2.2:', type=('build', 'run'))
