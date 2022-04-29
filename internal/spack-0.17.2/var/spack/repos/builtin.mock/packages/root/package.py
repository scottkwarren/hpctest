# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
class Root(Package):
    homepage = "http://www.example.com"
    url = "http://www.example.com/root-1.0.tar.gz"

    version('1.0', 'abcdef0123456789abcdef0123456789')

    depends_on('gmt')
