# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path


class LibtoolDeletion(AutotoolsPackage):
    """Mock AutotoolsPackage to check proper deletion
    of libtool archives.
    """
    homepage = "https://www.gnu.org/software/make/"
    url = "http://www.example.com/libtool-deletion-1.0.tar.gz"
    version('4.2.1', sha256='e40b8f018c1da64edd1cc9a6fce5fa63b2e707e404e20cad91fbae337c98a5b7')

    def do_stage(self):
        mkdirp(self.stage.source_path)

    def autoreconf(self, spec, prefix):
        mkdirp(os.path.dirname(self.configure_abs_path))
        touch(self.configure_abs_path)

    def configure(self, spec, prefix):
        pass

    def build(self, spec, prefix):
        pass

    def install(self, spec, prefix):
        mkdirp(os.path.dirname(self.libtool_archive_file))
        touch(self.libtool_archive_file)

    @property
    def libtool_archive_file(self):
        return os.path.join(str(self.prefix.lib), 'libfoo.la')
