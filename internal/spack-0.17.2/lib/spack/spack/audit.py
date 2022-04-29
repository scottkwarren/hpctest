# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Classes and functions to register audit checks for various parts of
Spack and run them on-demand.

To register a new class of sanity checks (e.g. sanity checks for
compilers.yaml), the first action required is to create a new AuditClass
object:

.. code-block:: python

   audit_cfgcmp = AuditClass(
       tag='CFG-COMPILER',
       description='Sanity checks on compilers.yaml',
       kwargs=()
   )

This object is to be used as a decorator to register functions
that will perform each a single check:

.. code-block:: python

   @audit_cfgcmp
   def _search_duplicate_compilers(error_cls):
       pass

These functions need to take as argument the keywords declared when
creating the decorator object plus an ``error_cls`` argument at the
end, acting as a factory to create Error objects. It should return a
(possibly empty) list of errors.

Calls to each of these functions are triggered by the ``run`` method of
the decorator object, that will forward the keyword arguments passed
as input.
"""
import collections
import itertools
import re

from six.moves.urllib.request import urlopen

try:
    from collections.abc import Sequence  # novm
except ImportError:
    from collections import Sequence


#: Map an audit tag to a list of callables implementing checks
CALLBACKS = {}

#: Map a group of checks to the list of related audit tags
GROUPS = collections.defaultdict(list)


class Error(object):
    """Information on an error reported in a test."""
    def __init__(self, summary, details):
        self.summary = summary
        self.details = tuple(details)

    def __str__(self):
        return self.summary + '\n' + '\n'.join([
            '    ' + detail for detail in self.details
        ])

    def __eq__(self, other):
        if self.summary != other.summary or self.details != other.details:
            return False
        return True

    def __hash__(self):
        value = (self.summary, self.details)
        return hash(value)


class AuditClass(Sequence):
    def __init__(self, group, tag, description, kwargs):
        """Return an object that acts as a decorator to register functions
        associated with a specific class of sanity checks.

        Args:
            group (str): group in which this check is to be inserted
            tag (str): tag uniquely identifying the class of sanity checks
            description (str): description of the sanity checks performed
                by this tag
            kwargs (tuple of str): keyword arguments that each registered
                function needs to accept
        """
        if tag in CALLBACKS:
            msg = 'audit class "{0}" already registered'
            raise ValueError(msg.format(tag))

        self.group = group
        self.tag = tag
        self.description = description
        self.kwargs = kwargs
        self.callbacks = []

        # Init the list of hooks
        CALLBACKS[self.tag] = self

        # Update the list of tags in the group
        GROUPS[self.group].append(self.tag)

    def __call__(self, func):
        self.callbacks.append(func)

    def __getitem__(self, item):
        return self.callbacks[item]

    def __len__(self):
        return len(self.callbacks)

    def run(self, **kwargs):
        msg = 'please pass "{0}" as keyword arguments'
        msg = msg.format(', '.join(self.kwargs))
        assert set(self.kwargs) == set(kwargs), msg

        errors = []
        kwargs['error_cls'] = Error
        for fn in self.callbacks:
            errors.extend(fn(**kwargs))

        return errors


def run_group(group, **kwargs):
    """Run the checks that are part of the group passed as argument.

    Args:
        group (str): group of checks to be run
        **kwargs: keyword arguments forwarded to the checks

    Returns:
        List of (tag, errors) that failed.
    """
    reports = []
    for check in GROUPS[group]:
        errors = run_check(check, **kwargs)
        reports.append((check, errors))
    return reports


def run_check(tag, **kwargs):
    """Run the checks associated with a single tag.

    Args:
        tag (str): tag of the check
        **kwargs: keyword arguments forwarded to the checks

    Returns:
        Errors occurred during the checks
    """
    return CALLBACKS[tag].run(**kwargs)


# TODO: For the generic check to be useful for end users,
# TODO: we need to implement hooks like described in
# TODO: https://github.com/spack/spack/pull/23053/files#r630265011
#: Generic checks relying on global state
generic = AuditClass(
    group='generic',
    tag='GENERIC',
    description='Generic checks relying on global variables',
    kwargs=()
)


#: Sanity checks on compilers.yaml
config_compiler = AuditClass(
    group='configs',
    tag='CFG-COMPILER',
    description='Sanity checks on compilers.yaml',
    kwargs=()
)


@config_compiler
def _search_duplicate_compilers(error_cls):
    """Report compilers with the same spec and two different definitions"""
    import spack.config
    errors = []

    compilers = list(sorted(
        spack.config.get('compilers'), key=lambda x: x['compiler']['spec']
    ))
    for spec, group in itertools.groupby(
            compilers, key=lambda x: x['compiler']['spec']
    ):
        group = list(group)
        if len(group) == 1:
            continue

        error_msg = 'Compiler defined multiple times: {0}'
        try:
            details = [str(x._start_mark).strip() for x in group]
        except Exception:
            details = []
        errors.append(error_cls(
            summary=error_msg.format(spec), details=details
        ))

    return errors


#: Sanity checks on packages.yaml
config_packages = AuditClass(
    group='configs',
    tag='CFG-PACKAGES',
    description='Sanity checks on packages.yaml',
    kwargs=()
)


@config_packages
def _search_duplicate_specs_in_externals(error_cls):
    """Search for duplicate specs declared as externals"""
    import spack.config

    errors, externals = [], collections.defaultdict(list)
    packages_yaml = spack.config.get('packages')

    for name, pkg_config in packages_yaml.items():
        # No externals can be declared under all
        if name == 'all' or 'externals' not in pkg_config:
            continue

        current_externals = pkg_config['externals']
        for entry in current_externals:
            # Ask for the string representation of the spec to normalize
            # aspects of the spec that may be represented in multiple ways
            # e.g. +foo or foo=true
            key = str(spack.spec.Spec(entry['spec']))
            externals[key].append(entry)

    for spec, entries in sorted(externals.items()):
        # If there's a single external for a spec we are fine
        if len(entries) < 2:
            continue

        # Otherwise wwe need to report an error
        error_msg = 'Multiple externals share the same spec: {0}'.format(spec)
        try:
            lines = [str(x._start_mark).strip() for x in entries]
            details = [
                'Please remove all but one of the following entries:'
            ] + lines + [
                'as they might result in non-deterministic hashes'
            ]
        except TypeError:
            details = []

        errors.append(error_cls(summary=error_msg, details=details))

    return errors


#: Sanity checks on package directives
package_directives = AuditClass(
    group='packages',
    tag='PKG-DIRECTIVES',
    description='Sanity checks on specs used in directives',
    kwargs=('pkgs',)
)

#: Sanity checks on linting
# This can take some time, so it's run separately from packages
package_https_directives = AuditClass(
    group='packages-https',
    tag='PKG-HTTPS-DIRECTIVES',
    description='Sanity checks on https checks of package urls, etc.',
    kwargs=('pkgs',)
)


@package_https_directives
def _linting_package_file(pkgs, error_cls):
    """Check for correctness of links
    """
    import llnl.util.lang

    import spack.repo
    import spack.spec

    errors = []
    for pkg_name in pkgs:
        pkg = spack.repo.get(pkg_name)

        # Does the homepage have http, and if so, does https work?
        if pkg.homepage.startswith('http://'):
            https = re.sub("http", "https", pkg.homepage, 1)
            try:
                response = urlopen(https)
            except Exception as e:
                msg = 'Error with attempting https for "{0}": '
                errors.append(error_cls(msg.format(pkg.name), [str(e)]))
                continue

            if response.getcode() == 200:
                msg = 'Package "{0}" uses http but has a valid https endpoint.'
                errors.append(msg.format(pkg.name))

    return llnl.util.lang.dedupe(errors)


@package_directives
def _unknown_variants_in_directives(pkgs, error_cls):
    """Report unknown or wrong variants in directives for this package"""
    import llnl.util.lang

    import spack.repo
    import spack.spec

    errors = []
    for pkg_name in pkgs:
        pkg = spack.repo.get(pkg_name)

        # Check "conflicts" directive
        for conflict, triggers in pkg.conflicts.items():
            for trigger, _ in triggers:
                vrn = spack.spec.Spec(conflict)
                try:
                    vrn.constrain(trigger)
                except Exception as e:
                    msg = 'Generic error in conflict for package "{0}": '
                    errors.append(error_cls(msg.format(pkg.name), [str(e)]))
                    continue
                errors.extend(_analyze_variants_in_directive(
                    pkg, vrn, directive='conflicts', error_cls=error_cls
                ))

        # Check "depends_on" directive
        for _, triggers in pkg.dependencies.items():
            triggers = list(triggers)
            for trigger in list(triggers):
                vrn = spack.spec.Spec(trigger)
                errors.extend(_analyze_variants_in_directive(
                    pkg, vrn, directive='depends_on', error_cls=error_cls
                ))

        # Check "patch" directive
        for _, triggers in pkg.provided.items():
            triggers = [spack.spec.Spec(x) for x in triggers]
            for vrn in triggers:
                errors.extend(_analyze_variants_in_directive(
                    pkg, vrn, directive='patch', error_cls=error_cls
                ))

        # Check "resource" directive
        for vrn in pkg.resources:
            errors.extend(_analyze_variants_in_directive(
                pkg, vrn, directive='resource', error_cls=error_cls
            ))

    return llnl.util.lang.dedupe(errors)


@package_directives
def _unknown_variants_in_dependencies(pkgs, error_cls):
    """Report unknown dependencies and wrong variants for dependencies"""
    import spack.repo
    import spack.spec

    errors = []
    for pkg_name in pkgs:
        pkg = spack.repo.get(pkg_name)
        filename = spack.repo.path.filename_for_package_name(pkg_name)
        for dependency_name, dependency_data in pkg.dependencies.items():
            # No need to analyze virtual packages
            if spack.repo.path.is_virtual(dependency_name):
                continue

            try:
                dependency_pkg = spack.repo.get(dependency_name)
            except spack.repo.UnknownPackageError:
                # This dependency is completely missing, so report
                # and continue the analysis
                summary = (pkg_name + ": unknown package '{0}' in "
                           "'depends_on' directive".format(dependency_name))
                details = [
                    " in " + filename
                ]
                errors.append(error_cls(summary=summary, details=details))
                continue

            for _, dependency_edge in dependency_data.items():
                dependency_variants = dependency_edge.spec.variants
                for name, value in dependency_variants.items():
                    try:
                        v, _ = dependency_pkg.variants[name]
                        v.validate_or_raise(value, pkg=dependency_pkg)
                    except Exception as e:
                        summary = (pkg_name + ": wrong variant used for a "
                                   "dependency in a 'depends_on' directive")
                        error_msg = str(e).strip()
                        if isinstance(e, KeyError):
                            error_msg = ('the variant {0} does not '
                                         'exist'.format(error_msg))
                        error_msg += " in package '" + dependency_name + "'"

                        errors.append(error_cls(
                            summary=summary, details=[error_msg, 'in ' + filename]
                        ))

    return errors


def _analyze_variants_in_directive(pkg, constraint, directive, error_cls):
    import spack.variant
    variant_exceptions = (
        spack.variant.InconsistentValidationError,
        spack.variant.MultipleValuesInExclusiveVariantError,
        spack.variant.InvalidVariantValueError,
        KeyError
    )
    errors = []
    for name, v in constraint.variants.items():
        try:
            variant, _ = pkg.variants[name]
            variant.validate_or_raise(v, pkg=pkg)
        except variant_exceptions as e:
            summary = pkg.name + ': wrong variant in "{0}" directive'
            summary = summary.format(directive)
            filename = spack.repo.path.filename_for_package_name(pkg.name)

            error_msg = str(e).strip()
            if isinstance(e, KeyError):
                error_msg = 'the variant {0} does not exist'.format(error_msg)

            err = error_cls(summary=summary, details=[
                error_msg, 'in ' + filename
            ])

            errors.append(err)

    return errors
