# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Detection of software installed in the system based on paths inspections
and running executables.
"""
import collections
import os
import os.path
import re

import llnl.util.filesystem
import llnl.util.tty

import spack.util.environment

from .common import (
    DetectedPackage,
    _convert_to_iterable,
    executable_prefix,
    is_executable,
)


def executables_in_path(path_hints=None):
    """Get the paths of all executables available from the current PATH.

    For convenience, this is constructed as a dictionary where the keys are
    the executable paths and the values are the names of the executables
    (i.e. the basename of the executable path).

    There may be multiple paths with the same basename. In this case it is
    assumed there are two different instances of the executable.

    Args:
        path_hints (list): list of paths to be searched. If None the list will be
            constructed based on the PATH environment variable.
    """
    path_hints = path_hints or spack.util.environment.get_path('PATH')
    search_paths = llnl.util.filesystem.search_paths_for_executables(*path_hints)

    path_to_exe = {}
    # Reverse order of search directories so that an exe in the first PATH
    # entry overrides later entries
    for search_path in reversed(search_paths):
        for exe in os.listdir(search_path):
            exe_path = os.path.join(search_path, exe)
            if is_executable(exe_path):
                path_to_exe[exe_path] = exe
    return path_to_exe


def _group_by_prefix(paths):
    groups = collections.defaultdict(set)
    for p in paths:
        groups[os.path.dirname(p)].add(p)
    return groups.items()


def by_executable(packages_to_check, path_hints=None):
    """Return the list of packages that have been detected on the system,
    searching by path.

    Args:
        packages_to_check (list): list of packages to be detected
        path_hints (list): list of paths to be searched. If None the list will be
            constructed based on the PATH environment variable.
    """
    path_to_exe_name = executables_in_path(path_hints=path_hints)
    exe_pattern_to_pkgs = collections.defaultdict(list)
    for pkg in packages_to_check:
        if hasattr(pkg, 'executables'):
            for exe in pkg.executables:
                exe_pattern_to_pkgs[exe].append(pkg)

    pkg_to_found_exes = collections.defaultdict(set)
    for exe_pattern, pkgs in exe_pattern_to_pkgs.items():
        compiled_re = re.compile(exe_pattern)
        for path, exe in path_to_exe_name.items():
            if compiled_re.search(exe):
                for pkg in pkgs:
                    pkg_to_found_exes[pkg].add(path)

    pkg_to_entries = collections.defaultdict(list)
    resolved_specs = {}  # spec -> exe found for the spec

    for pkg, exes in pkg_to_found_exes.items():
        if not hasattr(pkg, 'determine_spec_details'):
            llnl.util.tty.warn(
                "{0} must define 'determine_spec_details' in order"
                " for Spack to detect externally-provided instances"
                " of the package.".format(pkg.name))
            continue

        for prefix, exes_in_prefix in sorted(_group_by_prefix(exes)):
            # TODO: multiple instances of a package can live in the same
            # prefix, and a package implementation can return multiple specs
            # for one prefix, but without additional details (e.g. about the
            # naming scheme which differentiates them), the spec won't be
            # usable.
            specs = _convert_to_iterable(
                pkg.determine_spec_details(prefix, exes_in_prefix)
            )

            if not specs:
                llnl.util.tty.debug(
                    'The following executables in {0} were decidedly not '
                    'part of the package {1}: {2}'
                    .format(prefix, pkg.name, ', '.join(
                        _convert_to_iterable(exes_in_prefix)))
                )

            for spec in specs:
                pkg_prefix = executable_prefix(prefix)

                if not pkg_prefix:
                    msg = "no bin/ dir found in {0}. Cannot add it as a Spack package"
                    llnl.util.tty.debug(msg.format(prefix))
                    continue

                if spec in resolved_specs:
                    prior_prefix = ', '.join(
                        _convert_to_iterable(resolved_specs[spec]))

                    llnl.util.tty.debug(
                        "Executables in {0} and {1} are both associated"
                        " with the same spec {2}"
                        .format(prefix, prior_prefix, str(spec)))
                    continue
                else:
                    resolved_specs[spec] = prefix

                try:
                    spec.validate_detection()
                except Exception as e:
                    msg = ('"{0}" has been detected on the system but will '
                           'not be added to packages.yaml [reason={1}]')
                    llnl.util.tty.warn(msg.format(spec, str(e)))
                    continue

                if spec.external_path:
                    pkg_prefix = spec.external_path

                pkg_to_entries[pkg.name].append(
                    DetectedPackage(spec=spec, prefix=pkg_prefix)
                )

    return pkg_to_entries
