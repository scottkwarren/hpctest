# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyMsgpack(PythonPackage):
    """MessagePack (de)serializer."""

    homepage = "https://msgpack.org/"
    pypi = "msgpack/msgpack-1.0.0.tar.gz"

    version('1.0.2', sha256='fae04496f5bc150eefad4e9571d1a76c55d021325dcd484ce45065ebbdd00984')
    version('1.0.1', sha256='7033215267a0e9f60f4a5e4fb2228a932c404f237817caff8dc3115d9e7cd975')
    version('1.0.0', sha256='9534d5cc480d4aff720233411a1f765be90885750b07df772380b34c10ecb5c0')
    version('0.6.2', sha256='ea3c2f859346fcd55fc46e96885301d9c2f7a36d453f5d8f2967840efa1e1830')

    depends_on('py-setuptools', type='build')
