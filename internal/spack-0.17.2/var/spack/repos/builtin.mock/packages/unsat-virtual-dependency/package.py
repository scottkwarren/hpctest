# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
class UnsatVirtualDependency(Package):
    """This package has a dependency on a virtual that cannot be provided"""
    homepage = "http://www.example.com"
    url = "http://www.example.com/v1.0.tgz"

    version('1.0', sha256='0123456789abcdef0123456789abcdef')

    depends_on('unsatvdep')
