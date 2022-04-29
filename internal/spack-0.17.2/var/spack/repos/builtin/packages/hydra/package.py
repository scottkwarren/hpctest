# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hydra(AutotoolsPackage):
    """Hydra is a process management system for starting parallel jobs.
    Hydra is designed to natively work with existing launcher daemons
    (such as ssh, rsh, fork), as well as natively integrate with resource
    management systems (such as slurm, pbs, sge)."""

    homepage = "https://www.mpich.org"
    url      = "https://www.mpich.org/static/downloads/3.2/hydra-3.2.tar.gz"
    list_url = "https://www.mpich.org/static/downloads/"
    list_depth = 1

    version('3.2', sha256='f7a67ec91a773d95cbbd479a80e926d44bee1ff9fc70a8d1df075ea53ea33889')
