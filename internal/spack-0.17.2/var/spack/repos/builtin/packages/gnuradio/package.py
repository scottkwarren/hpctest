# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Gnuradio(CMakePackage):
    """GNU Radio is a free & open-source software development toolkit
    that provides signal processing blocks to implement software
    radios. It can be used with readily-available, low-cost external
    RF hardware to create software-defined radios, or without hardware
    in a simulation-like environment. It is widely used in hobbyist,
    academic, and commercial environments to support both wireless
    communications research and real-world radio systems."""

    homepage = "https://www.gnuradio.org/"
    url      = "https://github.com/gnuradio/gnuradio/archive/v3.8.2.0.tar.gz"

    maintainers = ['aweits']

    version('3.8.2.0', sha256='ddda12b55e3e1d925eefb24afb9d604bca7c9bbe0a431707aa48a2eed53eec2f')

    variant('gui', default=False, description='Build with gui support')

    depends_on('cmake@3.5.1:', type='build')
    depends_on('volk')
    depends_on('python@3.6.5:', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('swig@3.0.8:', type='build')
    depends_on('log4cpp@1.0:')
    # https://github.com/gnuradio/gnuradio/pull/3566
    depends_on('boost@1.53:1.72')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-click', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-click-plugins', type=('build', 'run'))
    depends_on('gsl@1.10:')
    depends_on('gmp')
    depends_on('fftw')
    depends_on('cppzmq')

    depends_on('cairo+X+ft+fc+pdf+gobject', when='+gui')
    depends_on('hicolor-icon-theme', type=('build', 'run'), when='+gui')
    depends_on('adwaita-icon-theme', type=('build', 'run'), when='+gui')
    depends_on('gsettings-desktop-schemas', type=('build', 'run'), when='+gui')
    depends_on('py-pygobject', type=('build', 'run'), when='+gui')
    depends_on('py-pyqt5', type=('build', 'run'), when='+gui')
    depends_on('qwt', when='+gui')

    extends('python')

    def cmake_args(self):
        args = []
        args.append('-DPYTHON_EXECUTABLE={0}'.format(
            self.spec['python'].command.path))
        args.append('-DENABLE_INTERNAL_VOLK=OFF')
        return args

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path('XDG_DATA_DIRS', self.prefix.share)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path('XDG_DATA_DIRS', self.prefix.share)

    def setup_build_environment(self, env):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)

    def setup_run_environment(self, env):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)
