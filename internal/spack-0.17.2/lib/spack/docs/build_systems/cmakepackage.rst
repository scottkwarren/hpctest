.. Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _cmakepackage:

------------
CMakePackage
------------

Like Autotools, CMake is a widely-used build-script generator. Designed
by Kitware, CMake is the most popular build system for new C, C++, and
Fortran projects, and many older projects are switching to it as well.

Unlike Autotools, CMake can generate build scripts for builders other
than Make: Ninja, Visual Studio, etc. It is therefore cross-platform,
whereas Autotools is Unix-only.

^^^^^^
Phases
^^^^^^

The ``CMakePackage`` base class comes with the following phases:

#. ``cmake`` - generate the Makefile
#. ``build`` - build the package
#. ``install`` - install the package

By default, these phases run:

.. code-block:: console

   $ mkdir spack-build
   $ cd spack-build
   $ cmake .. -DCMAKE_INSTALL_PREFIX=/path/to/installation/prefix
   $ make
   $ make test  # optional
   $ make install


A few more flags are passed to ``cmake`` by default, including flags
for setting the build type and flags for locating dependencies. Of
course, you may need to add a few arguments yourself.

^^^^^^^^^^^^^^^
Important files
^^^^^^^^^^^^^^^

A CMake-based package can be identified by the presence of a
``CMakeLists.txt`` file. This file defines the build flags that can be
passed to the cmake invocation, as well as linking instructions. If
you are familiar with CMake, it can prove very useful for determining
dependencies and dependency version requirements.

One thing to look for is the ``cmake_minimum_required`` function:

.. code-block:: cmake

   cmake_minimum_required(VERSION 2.8.12)


This means that CMake 2.8.12 is the earliest release that will work.
You should specify this in a ``depends_on`` statement.

CMake-based packages may also contain ``CMakeLists.txt`` in subdirectories.
This modularization helps to manage complex builds in a hierarchical
fashion. Sometimes these nested ``CMakeLists.txt`` require additional
dependencies not mentioned in the top-level file.

There's also usually a ``cmake`` or ``CMake`` directory containing
additional macros, find scripts, etc. These may prove useful in
determining dependency version requirements.

^^^^^^^^^^^^^^^^^^^^^^^^^
Build system dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^

Every package that uses the CMake build system requires a ``cmake``
dependency. Since this is always the case, the ``CMakePackage`` base
class already contains:

.. code-block:: python

   depends_on('cmake', type='build')


If you need to specify a particular version requirement, you can
override this in your package:

.. code-block:: python

   depends_on('cmake@2.8.12:', type='build')


^^^^^^^^^^^^^^^^^^^
Finding cmake flags
^^^^^^^^^^^^^^^^^^^

To get a list of valid flags that can be passed to ``cmake``, run the
following command in the directory that contains ``CMakeLists.txt``:

.. code-block:: console

   $ cmake . -LAH


CMake will start by checking for compilers and dependencies. Eventually
it will begin to list build options. You'll notice that most of the
build options at the top are prefixed with ``CMAKE_``. You can safely
ignore most of these options as Spack already sets them for you. This
includes flags needed to locate dependencies, RPATH libraries, set the
installation directory, and set the build type.

The rest of the flags are the ones you should consider adding to your
package. They often include flags to enable/disable support for certain
features and locate specific dependencies. One thing you'll notice that
makes CMake different from Autotools is that CMake has an understanding
of build flag hierarchy. That is, certain flags will not display unless
their parent flag has been selected. For example, flags to specify the
``lib`` and ``include`` directories for a package might not appear
unless CMake found the dependency it was looking for. You may need to
manually specify certain flags to explore the full depth of supported
build flags, or check the ``CMakeLists.txt`` yourself.

^^^^^^^^^^^^^^^^^^^^^
Adding flags to cmake
^^^^^^^^^^^^^^^^^^^^^

To add additional flags to the ``cmake`` call, simply override the
``cmake_args`` function. The following example defines values for the flags
``WHATEVER``, ``ENABLE_BROKEN_FEATURE``, ``DETECT_HDF5``, and ``THREADS`` with
and without the :meth:`~spack.build_systems.cmake.CMakePackage.define` and
:meth:`~spack.build_systems.cmake.CMakePackage.define_from_variant` helper functions:

.. code-block:: python

   def cmake_args(self):
       args = [
           '-DWHATEVER:STRING=somevalue',
           self.define('ENABLE_BROKEN_FEATURE', False),
           self.define_from_variant('DETECT_HDF5', 'hdf5'),
           self.define_from_variant('THREADS'), # True if +threads
       ]

       return args


^^^^^^^^^^
Generators
^^^^^^^^^^

CMake and Autotools are build-script generation tools; they "generate"
the Makefiles that are used to build a software package. CMake actually
supports multiple generators, not just Makefiles. Another common
generator is Ninja. To switch to the Ninja generator, simply add:

.. code-block:: python

   generator = 'Ninja'


``CMakePackage`` defaults to "Unix Makefiles". If you switch to the
Ninja generator, make sure to add:

.. code-block:: python

   depends_on('ninja', type='build')

to the package as well. Aside from that, you shouldn't need to do
anything else. Spack will automatically detect that you are using
Ninja and run:

.. code-block:: console

   $ cmake .. -G Ninja
   $ ninja
   $ ninja install

Spack currently only supports "Unix Makefiles" and "Ninja" as valid
generators, but it should be simple to add support for alternative
generators. For more information on CMake generators, see:
https://cmake.org/cmake/help/latest/manual/cmake-generators.7.html

^^^^^^^^^^^^^^^^
CMAKE_BUILD_TYPE
^^^^^^^^^^^^^^^^

Every CMake-based package accepts a ``-DCMAKE_BUILD_TYPE`` flag to
dictate which level of optimization to use. In order to ensure
uniformity across packages, the ``CMakePackage`` base class adds
a variant to control this:

.. code-block:: python

   variant('build_type', default='RelWithDebInfo',
           description='CMake build type',
           values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))

However, not every CMake package accepts all four of these options.
Grep the ``CMakeLists.txt`` file to see if the default values are
missing or replaced. For example, the
`dealii <https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/dealii/package.py>`_
package overrides the default variant with:

.. code-block:: python

   variant('build_type', default='DebugRelease',
           description='The build type to build',
           values=('Debug', 'Release', 'DebugRelease'))

For more information on ``CMAKE_BUILD_TYPE``, see:
https://cmake.org/cmake/help/latest/variable/CMAKE_BUILD_TYPE.html

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
CMakeLists.txt in a sub-directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Occasionally, developers will hide their source code and ``CMakeLists.txt``
in a subdirectory like ``src``. If this happens, Spack won't
be able to automatically detect the build system properly when running
``spack create``. You will have to manually change the package base
class and tell Spack where ``CMakeLists.txt`` resides. You can do this
like so:

.. code-block:: python

   root_cmakelists_dir = 'src'


Note that this path is relative to the root of the extracted tarball,
not to the ``build_directory``. It defaults to the current directory.

^^^^^^^^^^^^^^^^^^^^^^
Building out of source
^^^^^^^^^^^^^^^^^^^^^^

By default, Spack builds every ``CMakePackage`` in a ``spack-build``
sub-directory. If, for whatever reason, you would like to build in a
different sub-directory, simply override ``build_directory`` like so:

.. code-block:: python

   build_directory = 'my-build'

^^^^^^^^^^^^^^^^^^^^^^^^^
Build and install targets
^^^^^^^^^^^^^^^^^^^^^^^^^

For most CMake packages, the usual:

.. code-block:: console

   $ cmake
   $ make
   $ make install

is sufficient to install the package. However, if you need to run
make with any other targets, for example, to build an optional
library or build the documentation, you can add these like so:

.. code-block:: python

   build_targets = ['all', 'docs']
   install_targets = ['install', 'docs']

^^^^^^^
Testing
^^^^^^^

CMake-based packages typically provide unit testing via the
``test`` target. If you build your software with ``--test=root``,
Spack will check for the presence of a ``test`` target in the
Makefile and run ``make test`` for you. If you want to run a
different test instead, simply override the ``check`` method.

^^^^^^^^^^^^^^^^^^^^^^
External documentation
^^^^^^^^^^^^^^^^^^^^^^

For more information on the CMake build system, see:
https://cmake.org/cmake/help/latest/
