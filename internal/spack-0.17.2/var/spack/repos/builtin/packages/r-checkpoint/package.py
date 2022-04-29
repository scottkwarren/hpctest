# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCheckpoint(RPackage):
    """Install Packages from Snapshots on the Checkpoint Server for Reproducibility

    The goal of checkpoint is to solve the problem of package reproducibility
    in R. Specifically, checkpoint allows you to install packages as they
    existed on CRAN on a specific snapshot date as if you had a CRAN time
    machine. To achieve reproducibility, the checkpoint() function installs the
    packages required or called by your project and scripts to a local library
    exactly as they existed at the specified point in time. Only those packages
    are available to your project, thereby avoiding any package updates that
    came later and may have altered your results. In this way, anyone using
    checkpoint's checkpoint() can ensure the reproducibility of your scripts or
    projects at any time. To create the snapshot archives, once a day (at
    midnight UTC) Microsoft refreshes the Austria CRAN mirror on the "Microsoft
    R Archived Network" server (<https://mran.microsoft.com/>). Immediately
    after completion of the rsync mirror process, the process takes a snapshot,
    thus creating the archive. Snapshot archives exist starting from
    2014-09-17."""

    homepage = "https://cloud.r-project.org/package=checkpoint"
    url      = "https://cloud.r-project.org/src/contrib/checkpoint_0.4.6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/checkpoint"

    version('0.4.10', sha256='7362ae9703763fe4652d0b592cd913ce506f072a18e5cf5970d08d7cdf4d126a')
    version('0.4.6', sha256='fd1a5edb5cb1a40d7ed26bb196de566110fe2ef62e70b4e947c003576a03ebb2')
    version('0.4.3', sha256='c3e862f89f8838183d6028f7ed13683aec562e6dab77ad4b6a5e24ec653cfb64')
    version('0.3.15', sha256='09f1feeb2b5b8b409a2e16a9185827b8da5e555f1aa84442a287f15e452beed7')

    depends_on('r@3.0.0:', type=('build', 'run'))
