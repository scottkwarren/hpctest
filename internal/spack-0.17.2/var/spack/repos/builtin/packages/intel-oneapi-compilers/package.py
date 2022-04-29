# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import platform
import subprocess
from os import path

from spack import *


class IntelOneapiCompilers(IntelOneApiPackage):
    """Intel OneAPI compilers

    Provides Classic and Beta compilers for: Fortran, C, C++"""
    maintainers = ['rscohn2']

    homepage = "https://software.intel.com/content/www/us/en/develop/tools/oneapi.html"

    depends_on('patchelf', type='build')

    if platform.system() == 'Linux':
        version('2021.4.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18209/l_dpcpp-cpp-compiler_p_2021.4.0.3201_offline.sh',
                sha256='9206bff1c2fdeb1ca0d5f79def90dcf3e6c7d5711b9b5adecd96a2ba06503828',
                expand=False)
        resource(name='fortran-installer',
                 url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18210/l_fortran-compiler_p_2021.4.0.3224_offline.sh',
                 sha256='de2fcf40e296c2e882e1ddf2c45bb8d25aecfbeff2f75fcd7494068d621eb7e0',
                 expand=False,
                 placement='fortran-installer',
                 when='@2021.4.0')
        version('2021.3.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17928/l_dpcpp-cpp-compiler_p_2021.3.0.3168_offline.sh',
                sha256='f848d81b7cabc76c2841c9757abb2290921efd7b82491d830605f5785600e7a1',
                expand=False)
        resource(name='fortran-installer',
                 url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17959/l_fortran-compiler_p_2021.3.0.3168_offline.sh',
                 sha256='c4553f7e707be8e8e196f625e4e7fbc8eff5474f64ab85fc7146b5ed53ebc87c',
                 expand=False,
                 placement='fortran-installer',
                 when='@2021.3.0')
        version('2021.2.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17749/l_dpcpp-cpp-compiler_p_2021.2.0.118_offline.sh',
                sha256='5d01cbff1a574c3775510cd97ffddd27fdf56d06a6b0c89a826fb23da4336d59',
                expand=False)
        resource(name='fortran-installer',
                 url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17756/l_fortran-compiler_p_2021.2.0.136_offline.sh',
                 sha256='a62e04a80f6d2f05e67cd5acb03fa58857ee22c6bd581ec0651c0ccd5bdec5a1',
                 expand=False,
                 placement='fortran-installer',
                 when='@2021.2.0')
        version('2021.1.2',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17513/l_dpcpp-cpp-compiler_p_2021.1.2.63_offline.sh',
                sha256='68d6cb638091990e578e358131c859f3bbbbfbf975c581fd0b4b4d36476d6f0a',
                expand=False)
        resource(name='fortran-installer',
                 url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17508/l_fortran-compiler_p_2021.1.2.62_offline.sh',
                 sha256='29345145268d08a59fa7eb6e58c7522768466dd98f6d9754540d1a0803596829',
                 expand=False,
                 placement='fortran-installer',
                 when='@2021.1.2')

    @property
    def component_dir(self):
        return 'compiler'

    def _ld_library_path(self):
        dirs = ['lib',
                join_path('lib', 'x64'),
                join_path('lib', 'emu'),
                join_path('lib', 'oclfpga', 'host', 'linux64', 'lib'),
                join_path('lib', 'oclfpga', 'linux64', 'lib'),
                join_path('compiler', 'lib', 'intel64_lin'),
                join_path('compiler', 'lib')]
        for dir in dirs:
            yield join_path(self.component_path, 'linux', dir)

    def install(self, spec, prefix):
        # install cpp
        # Copy instead of install to speed up debugging
        # subprocess.run(f'cp -r /opt/intel/oneapi/compiler {prefix}', shell=True)
        super(IntelOneapiCompilers, self).install(spec, prefix)

        # install fortran
        super(IntelOneapiCompilers, self).install(
            spec,
            prefix,
            installer_path=glob.glob(join_path('fortran-installer', '*'))[0])

        # Some installers have a bug and do not return an error code when failing
        if not path.isfile(join_path(self.component_path, 'linux',
                                     'bin', 'intel64', 'ifort')):
            raise RuntimeError('install failed')

        # set rpath so 'spack compiler add' can check version strings
        # without setting LD_LIBRARY_PATH
        rpath = ':'.join(self._ld_library_path())
        patch_dirs = [join_path('compiler', 'lib', 'intel64_lin'),
                      join_path('compiler', 'lib', 'intel64'),
                      'bin']
        for pd in patch_dirs:
            patchables = glob.glob(join_path(self.component_path, 'linux', pd, '*'))
            patchables.append(join_path(self.component_path,
                                        'linux', 'lib', 'icx-lto.so'))
            for file in patchables:
                # Try to patch all files, patchelf will do nothing if
                # file should not be patched
                subprocess.call(['patchelf', '--set-rpath', rpath, file])
