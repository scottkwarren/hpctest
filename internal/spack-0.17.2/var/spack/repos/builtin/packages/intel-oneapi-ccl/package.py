# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack import *


class IntelOneapiCcl(IntelOneApiLibraryPackage):
    """Intel oneAPI CCL."""

    maintainers = ['rscohn2']

    homepage = 'https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/oneccl.html'

    depends_on('intel-oneapi-mpi')

    if platform.system() == 'Linux':
        version('2021.4.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18188/l_oneapi_ccl_p_2021.4.0.433_offline.sh',
                sha256='004031629d97ef99267d8ea962b666dc4be1560d7d32bd510f97bc81d9251ef6',
                expand=False)
        version('2021.3.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17920/l_oneapi_ccl_p_2021.3.0.343_offline.sh',
                sha256='0bb63e2077215cc161973b2e5029919c55e84aea7620ee9a848f6c2cc1245e3f',
                expand=False)
        version('2021.2.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17731/l_oneapi_ccl_p_2021.2.0.269_offline.sh',
                sha256='18b7875030243295b75471e235e91e5f7b4fc15caf18c07d941a6d47fba378d7',
                expand=False)
        version('2021.1.1',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17391/l_oneapi_ccl_p_2021.1.1.54_offline.sh',
                sha256='de732df57a03763a286106c8b885fd60e83d17906936a8897a384b874e773f49',
                expand=False)

    @property
    def component_dir(self):
        return 'ccl'
