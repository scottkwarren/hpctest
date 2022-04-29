# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Profugusmc(CMakePackage, CudaPackage):
    """ProfugusMC is a Monte Carlo radiation transport mini-app. It is designed
    to be a minimal, self-contained version of the Profugus application."""

    homepage = "https://code.ornl.gov/ProfugusMC/ProfugusMC"
    git = "https://code.ornl.gov/ProfugusMC/ProfugusMC.git"
    url = "https://code.ornl.gov/ProfugusMC/ProfugusMC/-/archive/master/ProfugusMC-master.tar.gz"

    version('master',  branch='master')

    variant('mpi', default=True, description='Enable MPI')
    variant('cuda', default=False, description='Enable CUDA')

    depends_on('blas')
    depends_on('lapack')
    depends_on('mpi', when='+mpi')
    depends_on('cuda', when='+cuda')
