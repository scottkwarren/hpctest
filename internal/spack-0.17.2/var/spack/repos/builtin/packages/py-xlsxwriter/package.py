# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyXlsxwriter(PythonPackage):
    """XlsxWriter is a Python module for writing files in the Excel 2007+ XLSX
       file format."""

    pypi = "XlsxWriter/XlsxWriter-1.0.2.tar.gz"

    version('1.0.2', sha256='a26bbbafff88abffce592ffd5dfaa4c9f08dc44ef4afbf45c70d3e270325f856')
