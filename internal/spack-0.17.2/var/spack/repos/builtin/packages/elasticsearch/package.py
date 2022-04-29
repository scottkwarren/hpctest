# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Elasticsearch(Package):
    """Elasticsearch is a search engine based on Lucene. It provides a
    distributed, multitenant-capable full-text search engine with an HTTP web
    interface and schema-free JSON documents.
    """

    homepage = "https://www.elastic.co/"
    url      = "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.2.4.tar.gz"

    version('6.4.0', sha256='e9786efb5cecd12adee2807c7640ba9a1ab3b484d2e87497bb8d0b6df0e24f01')
    version('6.3.0', sha256='0464127140820d82b24bd2830232131ea85bcd49267a8bc7365e4fa391dee2a3')
    version('6.2.4', sha256='91e6f1ea1e1dd39011e7a703d2751ca46ee374665b08b0bfe17e0c0c27000e8e')

    depends_on('java', type='run')

    def install(self, spec, prefix):
        dirs = [
            'bin',
            'config',
            'lib',
            'modules',
            'plugins']

        for d in dirs:
            install_tree(d, join_path(prefix, d))
