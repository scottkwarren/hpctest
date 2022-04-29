# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DepDiamondPatchMid1(Package):
    r"""Package that requires a patch on a dependency

  W
 / \
X   Y
 \ /
  Z

    This is package X
    """

    homepage = "http://www.example.com"
    url = "http://www.example.com/patch-a-dependency-1.0.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef')

    # single patch file in repo
    depends_on('patch', patches='mid1.patch')
