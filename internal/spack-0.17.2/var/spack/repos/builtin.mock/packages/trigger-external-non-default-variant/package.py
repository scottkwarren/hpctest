# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
class TriggerExternalNonDefaultVariant(Package):
    """This ackage depends on an external with a non-default variant"""
    homepage = "http://www.example.com"
    url = "http://www.someurl.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef')

    depends_on('external-non-default-variant')
