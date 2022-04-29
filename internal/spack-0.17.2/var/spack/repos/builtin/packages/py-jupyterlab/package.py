# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyJupyterlab(PythonPackage):
    """JupyterLab is the next-generation web-based user interface
       for Project Jupyter."""

    homepage = "https://github.com/jupyterlab/jupyterlab"
    pypi = "jupyterlab/jupyterlab-2.2.7.tar.gz"

    # Skip 'jupyterlab.tests' packages
    import_modules = ['jupyterlab', 'jupyterlab.handlers']

    version('3.2.1', sha256='54466941bcd9b52f23373a32038fbb4e50fd652d4536df6179b53e1ffb8ef431')
    version('3.1.18', sha256='a43733acc3729557fc4758cff55652e52896e42c64c1f12540656ae7f298b806')
    version('3.1.14', sha256='13174cb6076dd5da6f1b85725ccfcc9518d8f98e86b8b644fc89b1dfaeda63a9')
    version('3.0.18', sha256='0e4bb4b89014607a16658b54f13df2f0af14f3c286109a0e14d5a46cbbe28caf')
    version('3.0.16', sha256='7ad4fbe1f6d38255869410fd151a8b15692a663ca97c0a8146b3f5c40e275c23')
    version('3.0.14', sha256='713a84991dfcca8c0bc260911f1bd54ac25a386a86285713b9555a60f795059b')
    version('2.2.7', sha256='a72ffd0d919cba03a5ef8422bc92c3332a957ff97b0490494209c83ad93826da')
    version('2.1.0', sha256='8c239aababf5baa0b3d36e375fddeb9fd96f3a9a24a8cda098d6a414f5bbdc81')

    depends_on('python@3.6:', when='@3:', type=('build', 'run'))
    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-jupyter-packaging@0.9:1', when='@3.0.15:', type='build')
    depends_on('py-jupyter-packaging@0.7.3:0.7', when='@3.0.0:3.0.14', type=('build', 'run'))
    # dependency on py-jinja2@2.1 seems to be a migration issue from the switch
    # to setup.cfg in 3.0.15, leave it a 2.10
    depends_on('py-jinja2@2.10:', type=('build', 'run'))

    # @3:
    depends_on('py-ipython', when='@3:', type=('build', 'run'))
    depends_on('py-packaging', when='@3:', type=('build', 'run'))
    depends_on('py-tornado@6.1:', when='@3:', type=('build', 'run'))
    depends_on('py-jupyter-core', when='@3:', type=('build', 'run'))
    depends_on('py-jupyterlab-server@2.3:2', when='@3.0.9:', type=('build', 'run'))
    depends_on('py-jupyterlab-server@2.0:2', when='@3.0.0:3.0.8', type=('build', 'run'))
    depends_on('py-jupyter-server@1.4:1', when='@3.0.9:', type=('build', 'run'))
    depends_on('py-jupyter-server@1.2:1', when='@3.0.3:3.0.8', type=('build', 'run'))
    depends_on('py-jupyter-server@1.1:1', when='@3.0.0:3.0.2', type=('build', 'run'))
    depends_on('py-nbclassic@0.2.0:0', when='@3:', type=('build', 'run'))

    # @:3
    depends_on('py-notebook@4.3.1:', when='@:2', type=('build', 'run'))
    depends_on('py-tornado@:5,6.0.3:', when='@:2', type=('build', 'run'))
    depends_on('py-jupyterlab-server@1.1.5:1', when='@:2', type=('build', 'run'))

    def setup_run_environment(self, env):
        env.set('JUPYTERLAB_DIR', self.prefix.share.jupyter.lab)
