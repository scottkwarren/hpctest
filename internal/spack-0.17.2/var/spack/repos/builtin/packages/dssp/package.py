# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dssp(AutotoolsPackage):
    """'mkdssp' utility. (dictionary of protein secondary structure)"""

    homepage = "https://github.com/cmbi/dssp"
    url      = "https://github.com/cmbi/dssp/archive/3.1.4.tar.gz"

    version('3.1.4', sha256='496282b4b5defc55d111190ab9f1b615a9574a2f090e7cf5444521c747b272d4')
    version('2.3.0', sha256='4c95976d86dc64949cb0807fbd58c7bee5393df0001999405863dc90f05846c6')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('boost@1.48:')

    # pdb data download.
    # 1ALK.pdb - PDB (protein data bank) : https://www.rcsb.org/
    resource(
        name="pdb_data",
        url="https://files.rcsb.org/download/1ALK.pdb",
        sha256="99f4cd7ab63b35d64eacc85dc1491af5a03a1a0a89f2c9aadfb705c591b4b6c9",
        expand=False,
        placement='pdb'
    )

    def configure_args(self):
        args = [
            "--with-boost=%s" % self.spec['boost'].prefix]
        return args

    @run_after('configure')
    def edit(self):
        makefile = FileFilter(join_path(self.stage.source_path, 'Makefile'))
        makefile.filter('.*-Werror .*', '                    -Wno-error \\')

    @run_after('install')
    def cache_test_sources(self):
        """Save off the pdb sources for stand-alone testing."""
        self.cache_extra_test_sources('pdb')

    def test(self):
        """Perform stand-alone/smoke test on installed package."""
        pdb_path  = join_path(self.test_suite.current_test_cache_dir, 'pdb')
        self.run_test('mkdssp', options=['1ALK.pdb', '1alk.dssp'],
                      purpose='test: calculating structure for example',
                      installed=True,
                      work_dir=pdb_path)
