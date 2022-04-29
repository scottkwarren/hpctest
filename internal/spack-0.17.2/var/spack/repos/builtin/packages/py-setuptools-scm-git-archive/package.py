# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySetuptoolsScmGitArchive(PythonPackage):
    """This is a setuptools_scm plugin that adds support for git archives
       (for example the ones GitHub automatically generates)."""

    homepage = "https://github.com/Changaco/setuptools_scm_git_archive/"
    pypi = "setuptools_scm_git_archive/setuptools_scm_git_archive-1.1.tar.gz"

    maintainers = ['marcmengel']

    version(
        '1.1', sha256='6026f61089b73fa1b5ee737e95314f41cb512609b393530385ed281d0b46c062')
    version(
        '1.0', sha256='52425f905518247c685fc64c5fdba6e1e74443c8562e141c8de56059be0e31da')

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')
