# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dejagnu(AutotoolsPackage, GNUMirrorPackage):
    """DejaGnu is a framework for testing other programs. Its purpose
    is to provide a single front end for all tests."""

    homepage = "https://www.gnu.org/software/dejagnu/"
    gnu_mirror_path = "dejagnu/dejagnu-1.6.tar.gz"

    version('1.6',   sha256='00b64a618e2b6b581b16eb9131ee80f721baa2669fa0cdee93c500d1a652d763')
    version('1.4.4', sha256='d0fbedef20fb0843318d60551023631176b27ceb1e11de7468a971770d0e048d')

    depends_on('expect')
    depends_on('tcl@8.5:')

    # DejaGnu 1.4.4 cannot be built in parallel
    # `make check` also fails but this can be ignored
    parallel = False
