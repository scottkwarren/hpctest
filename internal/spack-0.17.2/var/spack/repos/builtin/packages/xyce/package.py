# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xyce(CMakePackage):
    """Xyce (rhymes with 'spice') is an open source, SPICE-compatible,
    high-performance analog circuit simulator, capable of solving extremely
    large circuit problems by supporting large-scale parallel computing
    platforms.
    Xyce also supports serial execution on all common desktop platforms,
    and small-scale parallel runs on Unix-like systems. In addition to analog
    electronic simulation, Xyce has also been used to investigate more general
    network systems, such as neural networks and power grids.
    """

    homepage = 'https://xyce.sandia.gov'
    git      = 'https://github.com/Xyce/Xyce.git'
    url      = 'https://github.com/Xyce/Xyce/archive/Release-7.2.0.tar.gz'
    maintainers = ['kuberry']

    version('github.master',  branch='master', preferred=True)
    version('7.3.0', '43869a70967f573ff6f00451db3f4642684834bdad1fd3926380e3789016b446')
    version('7.2.0', 'cf49705278ecda46373784bb24925cb97f9017b6adff49e4416de146bdd6a4b5')

    depends_on('cmake@3.13:', type='build')
    depends_on('flex')
    depends_on('bison')

    variant('build_type', default='Release',
            description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))

    variant('mpi', default=True, description='Enable MPI support')
    depends_on('mpi', when='+mpi')

    variant('pymi', default=False, description='Enable Python Model Interpreter for Xyce')
    depends_on('python@3:', type=('build', 'link', 'run'), when='+pymi')
    depends_on('py-pip', type='run', when='+pymi')
    depends_on('py-pybind11@2.6.1:', when='+pymi')

    # Xyce is built against an older version of Trilinos unlikely to be
    # used for any other purpose.
    depends_on('trilinos@12.12.1 +amesos+amesos2+anasazi+aztec+basker+belos+complex+epetra+epetraext+explicit_template_instantiation+fortran+hdf5+ifpack+isorropia+kokkos+nox+sacado+suite-sparse+trilinoscouplings+zoltan+stokhos+epetraextbtf+epetraextexperimental+epetraextgraphreorderings gotype=all')

    # Propagate variants to trilinos:
    for _variant in ('mpi',):
        depends_on('trilinos~' + _variant, when='~' + _variant)
        depends_on('trilinos+' + _variant, when='+' + _variant)

    # The default settings for various Trilinos variants would require the
    # installation of many more packages than are needed for Xyce.
    depends_on('trilinos~float~ifpack2~ml~muelu~zoltan2')

    def cmake_args(self):
        spec = self.spec

        trilinos = spec['trilinos']

        cxx_flags = [self.compiler.cxx_pic_flag]
        try:
            cxx_flags.append(self.compiler.cxx11_flag)
        except ValueError:
            pass
        cxx_flags.append("-DXyce_INTRUSIVE_PCE -Wreorder -O3")

        options = []
        options.extend([
            '-DTrilinos_DIR:PATH={0}'.format(trilinos.prefix),
            '-DCMAKE_CXX_FLAGS:STRING={0}'.format(' '.join(cxx_flags)),
        ])

        if '+mpi' in spec:
            options.append('-DCMAKE_CXX_COMPILER:STRING={0}'.format(spec['mpi'].mpicxx))
        else:
            options.append('-DCMAKE_CXX_COMPILER:STRING={0}'.format(self.compiler.cxx))

        if '+shared' in spec:
            options.append('-DBUILD_SHARED_LIBS:BOOL=ON')
        else:
            options.append('-DBUILD_SHARED_LIBS:BOOL=OFF')

        if '+pymi' in spec:
            pybind11 = spec['py-pybind11']
            python   = spec['python']
            options.append('-DXyce_PYMI:BOOL=ON')
            options.append('-Dpybind11_DIR:PATH={0}'.format(pybind11.prefix))
            options.append('-DPython_ROOT_DIR:FILEPATH={0}'.format(python.prefix))
            options.append('-DPython_FIND_STRATEGY=LOCATION')

        return options
