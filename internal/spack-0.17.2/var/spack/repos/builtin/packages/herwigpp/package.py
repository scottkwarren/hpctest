# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Herwigpp(AutotoolsPackage):
    """Herwig is a multi-purpose particle physics event generator.
       This package provides old Herwig++ 2 generator"""

    homepage = "https://herwig.hepforge.org/"
    url      = "http://lcgpackages.web.cern.ch/lcgpackages/tarFiles/sources/MCGeneratorsTarFiles/Herwig++-2.7.1.tar.bz2"

    tags = ['hep']

    version('2.7.1', '80a189376bb65f5ec4e64f42e76c00ea9102d8224010563a424fc11e619a6ad6')
    patch('herwig++-2.7.1.patch', when='@2.7.1', level=0)

    depends_on('gsl')
    depends_on('boost')
    depends_on('fastjet')
    depends_on('thepeg@1.9.2', when='@2.7.1')

    def configure_args(self):
        args = ['--with-gsl=' + self.spec['gsl'].prefix,
                '--with-thepeg=' + self.spec['thepeg'].prefix,
                '--with-fastjet=' + self.spec['fastjet'].prefix,
                '--with-boost=' + self.spec['boost'].prefix]
        return args

    def build(self, spec, prefix):
        make()
        with working_dir('Contrib'):
            make()

        with working_dir('Contrib/AlpGen'):
            make('BasicLesHouchesFileReader.so',
                 "HERWIGINCLUDE=-I{0}/include".format(self.stage.source_path))
            make('AlpGenHandler.so',
                 "HERWIGINCLUDE=-I{0}/include".format(self.stage.source_path))

    def install(self, spec, prefix):
        make('install')
        install(
            join_path(self.stage.source_path,
                      'Contrib', 'AlpGen', 'AlpGenHandler.so'),
            join_path(prefix.lib, 'Herwig++', 'AlpGenHandler.so'))

        install(
            join_path(self.stage.source_path,
                      'Contrib', 'AlpGen', 'BasicLesHouchesFileReader.so'),
            join_path(prefix.lib, 'Herwig++', 'BasicLesHouchesFileReader.so'))
