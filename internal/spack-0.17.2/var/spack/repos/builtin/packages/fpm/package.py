# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fpm(Package):
    """
    Fortran Package Manager (fpm) is a package manager and build system for Fortran.
    Its key goal is to improve the user experience of Fortran programmers.
    It does so by making it easier to build your Fortran program or library, run the
    executables, tests, and examples, and distribute it as a dependency to other
    Fortran projects.
    """

    homepage = "https://github.com/fortran-lang/fpm"
    url = "https://github.com/fortran-lang/fpm/releases/download/v0.4.0/fpm-0.4.0.zip"

    maintainers = ["awvwgk"]
    phases = ["install"]

    version("0.4.0", "cd9b80b7f40d9cf357ca8d5d4fe289fd32dfccb729bad7d2a68f245e4cdd0045")
    version("0.3.0", "3368d1b17e2d1368559174c796ce0e184cb6bf79c939938c6d166fbd15959fa3")

    variant("openmp", default=True, description="Use OpenMP parallelisation")

    depends_on("curl", type="build")

    def setup_build_environment(self, env):
        if "@0.4.0" in self.spec:
            env.set("FPM_C_COMPILER", self.compiler.cc)

        fflags = "-O3"
        if "+openmp" in self.spec:
            fflags += " " + self.compiler.openmp_flag
        env.set("FFLAGS", fflags)

    def install(self, spec, prefix):
        """
        A three step bootstrapping procedure to get the fpm binary:

        1. acquire single file source version of fpm (using curl)
        2. build bootstrap version from single file source version (using $FC)
        3. build full fpm version using bootstrap version

        This functionality is provided by the ``install.sh`` script.
        """

        script = Executable("./install.sh")
        script(*self.install_args())

    def install_args(self):
        args = ["--prefix={0}".format(self.prefix)]
        return args
