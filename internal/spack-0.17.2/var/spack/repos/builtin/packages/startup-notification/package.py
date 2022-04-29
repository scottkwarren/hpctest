# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class StartupNotification(AutotoolsPackage):
    """startup-notification contains a reference implementation of the
    freedesktop startup notification protocol."""

    homepage = "https://www.freedesktop.org/wiki/Software/startup-notification/"
    url      = "https://www.freedesktop.org/software/startup-notification/releases/startup-notification-0.12.tar.gz"

    version('0.12', sha256='3c391f7e930c583095045cd2d10eb73a64f085c7fde9d260f2652c7cb3cfbe4a')

    depends_on('libx11')
    depends_on('libxcb')
    depends_on('xcb-util')
