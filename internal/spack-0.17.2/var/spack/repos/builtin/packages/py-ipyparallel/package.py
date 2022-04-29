# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyIpyparallel(PythonPackage):
    """IPython's architecture for parallel and distributed computing."""

    homepage = "https://github.com/ipython/ipyparallel"
    pypi     = "ipyparallel/ipyparallel-7.1.0.tar.gz"

    version('7.1.0', sha256='ea756df0d2485bac19cccb0dbf4cafbc855c922b9b5905b4906e6cfac8b3c648')
    version('6.3.0', sha256='0a97b276c62db633e9e97a816282bdd166f9df74e28204f0c8fa54b71944cfdc')
    version('6.2.5', sha256='33416179665f9c2f567011ab1a618232bc32c0845c0a3a5c388f6c71048bc053')
    version('6.2.4', sha256='76c7b028962b0ba762e4e45b450ee3a4353e7221526a8af812e817d7ef6ac065')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('python@3.6:', type=('build', 'run'), when='@7.1.0:')

    depends_on('py-setuptools',        type='build')
    depends_on('py-jupyter-packaging', type='build')

    depends_on('py-ipython-genutils',     type=('build', 'run'), when='@:6.3.0')
    depends_on('py-decorator',            type=('build', 'run'))
    depends_on('py-pyzmq@13:',            type=('build', 'run'))
    depends_on('py-pyzmq@18:',            type=('build', 'run'), when='@7.1.0:')
    depends_on('py-traitlets@4.3:',       type=('build', 'run'))
    depends_on('py-ipython@4:',           type=('build', 'run'))
    depends_on('py-jupyter-client',       type=('build', 'run'))
    depends_on('py-ipykernel@4.4:',       type=('build', 'run'))
    depends_on('py-python-dateutil@2.1:', type=('build', 'run'))
    depends_on('py-tornado@4:',           type=('build', 'run'))
    depends_on('py-tornado@5.1:',         type=('build', 'run'), when='@7.1.0:')
    depends_on('py-entrypoints',          type=('build', 'run'), when='@7.1.0:')
    depends_on('py-psutil',               type=('build', 'run'), when='@7.1.0:')
    depends_on('py-tqdm',                 type=('build', 'run'), when='@7.1.0:')
