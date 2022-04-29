# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBokeh(PythonPackage):
    """Statistical and novel interactive HTML plots for Python"""

    homepage = "https://github.com/bokeh/bokeh"
    pypi = "bokeh/bokeh-0.12.2.tar.gz"

    version('2.4.1', sha256='d0410717d743a0ac251e62480e2ea860a7341bdcd1dbe01499a904f233c90512')
    version('2.4.0', sha256='6fa00ed8baab5cca33f4175792c309fa2536eaae7e90abee884501ba8c90fddb')
    version('2.3.3', sha256='a5fdcc181835561447fcc5a371300973fce4114692d5853addec284d1cdeb677')
    version('1.3.4', sha256='e2d97bed5b199a10686486001fed5c854e4c04ebe28859923f27c52b93904754')
    version('0.12.2', sha256='0a840f6267b6d342e1bd720deee30b693989538c49644142521d247c0f2e6939')

    depends_on('py-setuptools', type='build', when="@1.3.4:")

    depends_on('python@2.6:',             type=('build', 'run'), when='@0.12.2')
    depends_on('python@2.7:',             type=('build', 'run'), when='@1.3.4:')
    depends_on('python@3.6:',             type=('build', 'run'), when='@2.3.3:')
    depends_on('python@3.7:',             type=('build', 'run'), when='@2.4.0:')

    depends_on('py-requests@1.2.3:',      type=('build', 'run'), when='@0.12.2')

    depends_on('py-packaging@16.8:',      type=('build', 'run'), when='@1.3.4:')
    depends_on('py-six@1.5.2:',           type=('build', 'run'), when='@:1.3.4')
    depends_on('py-pyyaml@3.10:',         type=('build', 'run'))
    depends_on('py-python-dateutil@2.1:', type=('build', 'run'), when='@:2.3.3')
    depends_on('py-futures@3.0.3:',       type=('build', 'run'), when='@:1.3.4 ^python@2.7:2.8')

    depends_on('pil@4.0:',                type=('build', 'run'), when='@1.3.4:')
    depends_on('pil@7.1.0:',              type=('build', 'run'), when='@2.3.3:')

    depends_on('py-jinja2@2.7:',          type=('build', 'run'))
    depends_on('py-jinja2@2.9:',          type=('build', 'run'), when='@2.3.3:')

    depends_on('py-numpy@1.7.1:',         type=('build', 'run'))
    depends_on('py-numpy@1.11.3:',        type=('build', 'run'), when='@2.3.3:')

    depends_on('py-tornado@4.3:',         type=('build', 'run'))
    depends_on('py-tornado@5.1:',         type=('build', 'run'), when='@2.3.3:')

    depends_on('py-typing-extensions@3.7.4:', type=('build', 'run'), when='@2.3.3:')
    depends_on('py-typing-extensions@3.10.0:', type=('build', 'run'), when='@2.4.0:')
