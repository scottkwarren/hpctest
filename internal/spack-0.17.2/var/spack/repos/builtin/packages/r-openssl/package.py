# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ROpenssl(RPackage):
    """Toolkit for Encryption, Signatures and Certificates Based on OpenSSL

    Bindings to OpenSSL libssl and libcrypto, plus custom SSH pubkey
    parsers. Supports RSA, DSA and EC curves P-256, P-384 and P-521.
    Cryptographic signatures can either be created and verified manually or via
    x509 certificates. AES can be used in cbc, ctr or gcm mode for symmetric
    encryption; RSA for asymmetric (public key) encryption or EC for Diffie
    Hellman. High-level envelope functions combine RSA and AES for encrypting
    arbitrary sized data. Other utilities include key generators, hash
    functions (md5, sha1, sha256, etc), base64 encoder, a secure random number
    generator, and 'bignum' math methods for manually performing crypto
    calculations on large multibyte integers."""

    homepage = "https://cloud.r-project.org/package=openssl"
    cran = "openssl"

    version('1.4.5', sha256='4fc141aba8e94e9f5ecce6eda07e45a5e7048d8609ba909ede4f7f4933e0c1f7')
    version('1.4.3', sha256='342001df8ecff5df2cdf757f123d35ea4b449751045f708b91f27c1be0d48269')
    version('1.4.1', sha256='f7fbecc75254fc43297a95a4338c674ab9ba2ec056b59e027d16d23122161fc6')
    version('1.3', sha256='1c83f4d529adc1f5ec40e477c690a8d5b0a42422f3e542f1fc39062dcfaca4bf')
    version('0.9.7', sha256='697d9e86f99270163744538dc3dc4d19d00af89a8570a1d304b110e1d2650e9d')
    version('0.9.6', sha256='6dd6d1cade4004962d516ad761fff0812beec0232318b385d286761423a5dc39')
    version('0.9.4', sha256='cb7349defa5428acc0907629a4f53f82d2519af219e5d6a41f852cf55b1feb66')

    depends_on('r-askpass', when='@1.2:', type=('build', 'run'))
    depends_on('openssl@1.0.1:')

    def flag_handler(self, name, flags):
        if name == 'cflags':
            flags.append(self.compiler.c99_flag)
        return (flags, None, None)
