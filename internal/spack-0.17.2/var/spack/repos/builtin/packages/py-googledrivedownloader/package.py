# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyGoogledrivedownloader(PythonPackage):
    """Minimal class to download shared files from Google Drive."""

    homepage = "https://github.com/ndrplz/google-drive-downloader"
    pypi = "googledrivedownloader/googledrivedownloader-0.4.tar.gz"

    version('0.4', sha256='4b34c1337b2ff3bf2bd7581818efbdcaea7d50ffd484ccf80809688f5ca0e204')

    depends_on('py-setuptools', type='build')
