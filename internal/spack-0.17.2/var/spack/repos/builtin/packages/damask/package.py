# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Damask(BundlePackage):
    """
    DAMASK - The Duesseldorf Advanced Material Simulation Kit

    A unified multi-physics crystal plasticity simulation package. The solution of
    continuum mechanical boundary value problems requires a constitutive response
    that connects deformation and stress at each material point. This problem is
    solved in DAMASK on the basis of crystal plasticity using a variety of constitutive
    models and homogenization approaches. However, treating mechanics in isolation is
    no longer sufficient to study emergent advanced high-strength materials. In these
    materials, deformation happens interrelated with displacive phase transformation,
    significant heating, and potential damage evolution. Therefore, DAMASK is capable
    of handling multi-physics problems. Following a modular approach, additional field
    equations are solved in a fully coupled way using a staggered approach.

    """

    homepage = "https://damask3.mpie.de"

    maintainers = ['MarDiehl']

    version('3.0.0-alpha4')
    version('3.0.0-alpha5')

    depends_on('damask-grid@3.0.0-alpha4', when='@3.0.0-alpha4', type='run')
    depends_on('damask-mesh@3.0.0-alpha4', when='@3.0.0-alpha4', type='run')
    depends_on('py-damask@3.0.0-alpha4',   when='@3.0.0-alpha4', type='run')

    depends_on('damask-grid@3.0.0-alpha5', when='@3.0.0-alpha5', type='run')
    depends_on('damask-mesh@3.0.0-alpha5', when='@3.0.0-alpha5', type='run')
    depends_on('py-damask@3.0.0-alpha5',   when='@3.0.0-alpha5', type='run')
