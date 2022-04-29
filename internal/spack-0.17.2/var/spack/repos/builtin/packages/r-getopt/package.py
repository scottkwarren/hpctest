# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGetopt(RPackage):
    """Package designed to be used with Rscript to write "#!" shebang scripts
       that accept short and long flags/options. Many users will prefer using
       instead the packages optparse or argparse which add extra features like
       automatically generated help option and usage, support for default
       values, positional argument support, etc."""

    homepage = "https://github.com/trevorld/getopt"
    url      = "https://cloud.r-project.org/src/contrib/getopt_1.20.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/getopt"

    version('1.20.3', sha256='531f5fdfdcd6b96a73df2b39928418de342160ac1b0043861e9ea844f9fbf57f')
    version('1.20.2', sha256='3d6c12d32d6cd4b2909be626e570e158b3ed960e4739510e3a251e7f172de38e')
    version('1.20.1', sha256='1522c35b13e8546979725a68b75e3bc9d156fb06569067472405f6b8591d8654')
