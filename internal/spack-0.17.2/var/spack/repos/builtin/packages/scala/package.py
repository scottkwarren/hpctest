# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Scala(Package):
    """Scala is a general-purpose programming language providing support for
    functional programming and a strong static type system. Designed to be
    concise, many of Scala's design decisions were designed to build from
    criticisms of Java.
    """

    homepage = "https://www.scala-lang.org/"
    url = "https://downloads.lightbend.com/scala/2.12.1/scala-2.12.1.tgz"

    version('2.13.1',  sha256='6918ccc494e34810a7254ad2c4e6f0e1183784c22e7b4801b7dbc8d1994a04db')
    version('2.12.10', sha256='3b12bda3300fedd91f64fc7f9165fd45c58328b1b760af24ca6ffe92e3b0656a')
    version('2.12.6', sha256='1ac7444c5a85ed1ea45db4a268ee9ea43adf80e7f5724222863afb5492883416')
    version('2.12.5', sha256='b261ffe9a495b12e9dda2ed37331e579547e4d1b8b5810161b6c3b39ac806aa1')
    version('2.12.1', sha256='4db068884532a3e27010df17befaca0f06ea50f69433d58e06a5e63c7a3cc359')
    version('2.11.11', sha256='12037ca64c68468e717e950f47fc77d5ceae5e74e3bdca56f6d02fd5bfd6900b')
    version('2.10.6', sha256='54adf583dae6734d66328cafa26d9fa03b8c4cf607e27b9f3915f96e9bcd2d67')

    depends_on('java')

    def install(self, spec, prefix):

        def install_dir(dirname):
            install_tree(dirname, join_path(prefix, dirname))

        install_dir('bin')
        install_dir('lib')
        install_dir('doc')
        install_dir('man')
