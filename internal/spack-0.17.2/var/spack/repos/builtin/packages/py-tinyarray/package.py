# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTinyarray(PythonPackage):
    """Tinyarrays are similar to NumPy arrays, but optimized for
    small sizes. Common operations on very small arrays are to 3-7
    times faster than with NumPy (with NumPy 1.6 it used to be up
    to 35 times), and 3 times less memory is used to store them.
    Tinyarrays are useful if you need many small arrays of numbers,
    and cannot combine them into a few large ones."""

    homepage = "https://gitlab.kwant-project.org/kwant/tinyarray"
    url = "https://downloads.kwant-project.org/tinyarray/tinyarray-1.2.3.tar.gz"
    git = "https://gitlab.kwant-project.org/kwant/tinyarray"

    # Add a list of GitHub accounts to notify when the
    # package is updated
    maintainers = ['payerle']

    version('1.2.3', sha256='47a06f801ed4b3d438f4f7098e244cd0c6d7db09428b1bc5ee813e52234dee9f')
    version('1.2.2', sha256='660d6d8532e1db5efbebae2861e5733a7082486fbdeb47d57d84b8f477d697e4')
    version('1.2.1', sha256='47a06f801ed4b3d438f4f7098e244cd0c6d7db09428b1bc5ee813e52234dee9f')

    depends_on('py-setuptools', type='build')
