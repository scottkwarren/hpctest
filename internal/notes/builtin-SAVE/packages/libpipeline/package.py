##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Libpipeline(AutotoolsPackage):
    """libpipeline is a C library for manipulating pipelines of subprocesses
    in a flexible and convenient way."""

    homepage = "http://libpipeline.nongnu.org/"
    url      = "http://git.savannah.nongnu.org/cgit/libpipeline.git/snapshot/libpipeline-1.4.2.tar.gz"

    version('1.4.2', '30cec7bcd6fee723adea6a54389f3da2')

    depends_on('pkg-config', type='build')
    # TODO: Add a 'test' deptype
    # See https://github.com/spack/spack/issues/1279
    # depends_on('check', type='test')
