# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Opendx(AutotoolsPackage):
    """Open Visualization Data Explorer."""

    homepage = "https://github.com/Mwoolsey/OpenDX"
    git      = "https://github.com/Mwoolsey/OpenDX.git"

    version('master', branch='master')

    depends_on('motif')  # lesstif also works, but exhibits odd behaviors
    depends_on('gl')

    @run_before('autoreconf')
    def distclean(self):
        make('distclean')
