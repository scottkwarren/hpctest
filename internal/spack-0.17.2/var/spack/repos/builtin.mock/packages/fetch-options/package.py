# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FetchOptions(Package):
    """Mock package with fetch_options."""

    homepage = "http://www.fetch-options-example.com"

    url = 'https://example.com/some/tarball-1.0.tar.gz'

    fetch_options = {'timeout': 42, 'cookie': 'foobar'}
    timeout = {'timeout': 65}
    cookie = {'cookie': 'baz'}

    version('1.2', '00000000000000000000000000000012', fetch_options=cookie)
    version('1.1', '00000000000000000000000000000011', fetch_options=timeout)
    version('1.0', '00000000000000000000000000000010')
