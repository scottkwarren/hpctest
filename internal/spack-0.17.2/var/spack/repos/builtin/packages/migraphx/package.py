# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Migraphx(CMakePackage):
    """ AMD's graph optimization engine."""

    homepage = "https://github.com/ROCmSoftwarePlatform/AMDMIGraphX"
    git      = "https://github.com/ROCmSoftwarePlatform/AMDMIGraphX.git"
    url = "https://github.com/ROCmSoftwarePlatform/AMDMIGraphX/archive/rocm-4.3.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('4.3.1', sha256='e0b04da37aed937a2b2218059c189559a15460c191b5e9b00c7366c81c90b06e')
    version('4.3.0', sha256='99cf202a5e86cf5502b0f8bf12f152dbd5a6aacc204b3d9d5efca67a54793408')
    version('4.2.0', sha256='93f22f6c641dde5d7fb8abcbd99621b3c81e332e125a6f3a258d5e4cf2055f55')
    version('4.1.0', sha256='f9b1d2e25cdbaf5d0bfb07d4c8ccef0abaa291757c4bce296c3b5b9488174045')
    version('4.0.0', sha256='b8b845249626e9169353dbfa2530db468972a7569b248c8118ff19e029a12e55')
    version('3.10.0', sha256='eda22b9af286afb7806e6b5d5ebb0d612dce87c9bad64ba5176fda1c2ed9c9b7')
    version('3.9.0', sha256='7649689e06522302c07b39abb88bdcc3d4de18a7559d4f6a9e238e92b2074032')
    version('3.8.0', sha256='08fa991349a2b95364b0a69be7960580c3e3fde2fda0f0c67bc41429ea2d67a0')
    version('3.7.0', sha256='697c3c7babaa025eaabec630dbd8a87d10dc4fe35fafa3b0d3463aaf1fc46399')
    version('3.5.0', sha256='5766f3b262468c500be5051a056811a8edfa741734a5c08c4ecb0337b7906377')

    def url_for_version(self, version):
        url = "https://github.com/ROCmSoftwarePlatform/AMDMIGraphX/archive/"
        if version <= Version('3.5.0'):
            url += "{0}.tar.gz".format(version)
        else:
            url += "rocm-{0}.tar.gz".format(version)

        return url

    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')

    patch('0001-Adding-nlohmann-json-include-directory.patch', when='@3.9.0:')

    depends_on('cmake@3:', type='build')
    depends_on('protobuf', type='link')
    depends_on('blaze', type='build')
    depends_on('nlohmann-json', type='link')
    depends_on('msgpack-c', type='link')
    depends_on('half@1.12.0', type='link')
    depends_on('python@3:', type='build')
    depends_on('py-pybind11', type='build', when='@:4.0.0')
    depends_on('py-pybind11@2.6:', type='build', when='@4.1.0:')

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1']:
        depends_on('rocm-cmake@' + ver, type='build', when='@' + ver)
        depends_on('hip@' + ver,                      when='@' + ver)
        depends_on('llvm-amdgpu@' + ver,              when='@' + ver)
        depends_on('rocblas@' + ver,                  when='@' + ver)
        depends_on('miopen-hip@' + ver,               when='@' + ver)

    @property
    def cmake_python_hints(self):
        """Include the python include path to the
        CMake based on current spec
        """
        python_spec = self.spec['python']
        include_dir = join_path(
            python_spec.prefix, python_spec.package.config_vars['python_inc']['false'])
        return [
            self.define('Python_INCLUDE_DIR', include_dir)
        ]

    def cmake_args(self):
        args = [
            '-DCMAKE_CXX_COMPILER={0}/bin/clang++'
            .format(self.spec['llvm-amdgpu'].prefix)
        ]
        if '@3.9.0:' in self.spec:
            args.append('-DNLOHMANN_JSON_INCLUDE={0}'.format(
                self.spec['nlohmann-json'].prefix.include))

        if self.spec['cmake'].satisfies('@3.16.0:'):
            args += self.cmake_python_hints
        return args
