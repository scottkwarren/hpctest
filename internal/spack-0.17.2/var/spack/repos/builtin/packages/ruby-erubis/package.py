# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class RubyErubis(RubyPackage):
    """Erubis is a fast, secure, and very extensible implementation of eRuby.
    """

    homepage = "http://www.kuwata-lab.com/erubis/"
    git      = "https://github.com/kwatch/erubis.git"

    version('master', branch='master')
    version('2.7.0', commit='14d3eab57fbc361312c8f3af350cbf9a5bafce17')

    def patch(self):
        filter_file('$Release$', str(self.version),
                    'erubis.gemspec', string=True)
