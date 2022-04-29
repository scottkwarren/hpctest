# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkg.builtin.mock.patch import Patch


class PatchInheritance(Patch):
    def install(self, spec, prefix):
        Patch.install(self, spec, prefix)
