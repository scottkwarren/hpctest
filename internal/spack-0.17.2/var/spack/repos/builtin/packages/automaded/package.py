# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Automaded(CMakePackage):
    """AutomaDeD (Automata-based Debugging for Dissimilar parallel
       tasks) is a tool for automatic diagnosis of performance and
       correctness problems in MPI applications. It creates
       control-flow models of each MPI process and, when a failure
       occurs, these models are leveraged to find the origin of
       problems automatically. MPI calls are intercepted (using
       wrappers) to create the models. When an MPI application hangs,
       AutomaDeD creates a progress-dependence graph that helps
       finding the process (or group of processes) that caused the hang.
    """

    homepage = "https://github.com/llnl/AutomaDeD"
    url      = "https://github.com/llnl/AutomaDeD/archive/v1.0.tar.gz"

    version('1.0', sha256='600740cdd594cc6968c7bcb285d0829eb0ddbd5597c32c06c6ae5d9929a2625d')

    depends_on('mpi')
    depends_on('boost')
    depends_on('callpath')
    depends_on('cmake@2.8:', type='build')

    def cmake_args(self):
        return ['-DSTATE_TRACKER_WITH_CALLPATH=ON']
