# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyTransformers(PythonPackage):
    """State-of-the-art Natural Language Processing for TensorFlow 2.0 and
    PyTorch"""

    homepage = "https://github.com/huggingface/transformers"
    pypi = "transformers/transformers-2.8.0.tar.gz"

    maintainers = ['adamjstewart']

    version('4.6.1', sha256='83dbff763b7e7dc57cbef1a6b849655d4fcab6bffdd955c5e8bea12a4f76dc10')
    version('2.8.0', sha256='b9f29cdfd39c28f29e0806c321270dea337d6174a7aa60daf9625bf83dbb12ee')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-numpy@1.17:', when='@4.6.1:', type=('build', 'run'))

    depends_on('py-tokenizers', type=('build', 'run'))
    depends_on('py-tokenizers@0.10.1:0.10', when='@4.6.1:', type=('build', 'run'))

    depends_on('py-dataclasses', when='^python@:3.6', type=('build', 'run'))
    depends_on('py-boto3', when='@2.8.0', type=('build', 'run'))
    depends_on('py-filelock', type=('build', 'run'))
    depends_on('py-requests', type=('build', 'run'))
    depends_on('py-tqdm@4.27:', type=('build', 'run'))
    depends_on('py-regex@:2019.12.16,2019.12.18:', type=('build', 'run'))

    depends_on('py-sentencepiece', type=('build', 'run'))
    depends_on('py-sentencepiece@0.1.91', when='@4.6.1:', type=('build', 'run'))

    depends_on('py-sacremoses', type=('build', 'run'))
    depends_on('py-importlib-metadata', when='@4.6.1: ^python@:3.7', type=('build', 'run'))
    depends_on('py-huggingface-hub@0.0.8', when='@4.6.1:', type=('build', 'run'))
    depends_on('py-packaging', when='@4.6.1:', type=('build', 'run'))
