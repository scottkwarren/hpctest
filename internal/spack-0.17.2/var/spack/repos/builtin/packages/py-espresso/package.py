# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyEspresso(CMakePackage):
    """ESPResSo is a highly versatile software package for performing and
       analyzing scientific Molecular Dynamics many-particle simulations of
       coarse-grained atomistic or bead-spring models as they are used in
       soft matter research in physics, chemistry and molecular biology. It
       can be used to simulate systems such as polymers, liquid crystals,
       colloids, polyelectrolytes, ferrofluids and biological systems, for
       example DNA and lipid membranes. It also has a DPD and lattice
       Boltzmann solver for hydrodynamic interactions, and allows several
       particle couplings to the LB fluid.
    """
    homepage = "https://espressomd.org/"
    git      = "https://github.com/espressomd/espresso.git"
    url      = "https://github.com/espressomd/espresso/releases/download/4.0.0/espresso-4.0.0.tar.gz"

    version('develop', branch='python')
    version('4.0.2', sha256='89878ab44a58e90b69d56368e961b8ca13d9307f8d4b282967a1f3071a62c740')
    version('4.0.1', sha256='17b7268eeba652a77f861bc534cdd05d206e7641d203a9dd5029b44bd422304b')
    version('4.0.0', sha256='8e128847447eebd843de24be9b4ad14aa19c028ae48879a5a4535a9683836e6b')

    # espressomd/espresso#2244 merge upstream
    patch('2244.patch', when="@4.0.0")

    depends_on("cmake@3.0:", type='build')
    depends_on("mpi")
    depends_on("boost+serialization+filesystem+system+python+mpi")
    extends("python")
    depends_on("py-cython@0.23:", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("fftw")
    depends_on("hdf5+hl+mpi")
