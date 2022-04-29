# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Grads(AutotoolsPackage):
    """The Grid Analysis and Display System (GrADS) is an interactive
    desktop tool that is used for easy access, manipulation, and visualization
    of earth science data. GrADS has two data models for handling gridded and
    station data. GrADS supports many data file formats, including
    binary (stream or sequential), GRIB (version 1 and 2), NetCDF,
    HDF (version 4 and 5), and BUFR (for station data)."""

    homepage = "http://cola.gmu.edu/grads/grads.php"
    url      = "ftp://cola.gmu.edu/grads/2.2/grads-2.2.1-src.tar.gz"

    version('2.2.1', sha256='695e2066d7d131720d598bac0beb61ac3ae5578240a5437401dc0ffbbe516206')

    variant('geotiff', default=True, description="Enable GeoTIFF support")
    variant('shapefile', default=True, description="Enable Shapefile support")

    """
    # FIXME: Fails with undeclared functions (tdefi, tdef, ...) in gauser.c
    variant('hdf5', default=False, description="Enable HDF5 support")
    variant('hdf4', default=False, description="Enable HDF4 support")
    variant('netcdf', default=False, description="Enable NetCDF support")
    depends_on('hdf5', when='+hdf5')
    depends_on('hdf', when='+hdf4')
    depends_on('netcdf-c', when='+netcdf')
    """

    depends_on('libgeotiff', when='+geotiff')
    depends_on('shapelib', when='+shapefile')
    depends_on('udunits')
    depends_on('libgd')
    depends_on('libxmu')
    depends_on('cairo +X +pdf +fc +ft')
    depends_on('readline')
    depends_on('pkgconfig', type='build')

    def setup_build_environment(self, env):
        env.set('SUPPLIBS', '/')

    def setup_run_environment(self, env):
        env.set('GADDIR', self.prefix.data)

    @run_after('install')
    def copy_data(self):
        with working_dir(self.build_directory):
            install_tree('data', self.prefix.data)
        with working_dir(self.package_dir):
            install('udpt', self.prefix.data)
            filter_file(
                r'({lib})',
                self.prefix.lib,
                self.prefix.data.udpt
            )

    def configure_args(self):
        args = []
        args.extend(self.with_or_without('geotiff'))
        return args
