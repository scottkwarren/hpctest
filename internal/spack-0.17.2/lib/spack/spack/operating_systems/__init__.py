# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from ._operating_system import OperatingSystem
from .cray_backend import CrayBackend
from .cray_frontend import CrayFrontend
from .linux_distro import LinuxDistro
from .mac_os import MacOs

__all__ = [
    'OperatingSystem',
    'LinuxDistro',
    'MacOs',
    'CrayFrontend',
    'CrayBackend'
]

#: List of all the Operating Systems known to Spack
operating_systems = [LinuxDistro, MacOs, CrayFrontend, CrayBackend]
