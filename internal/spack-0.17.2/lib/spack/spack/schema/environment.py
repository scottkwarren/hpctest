# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Schema for environment modifications. Meant for inclusion in other
schemas.
"""

array_of_strings_or_num = {
    'type': 'array', 'default': [], 'items':
        {'anyOf': [{'type': 'string'}, {'type': 'number'}]}
}

dictionary_of_strings_or_num = {
    'type': 'object', 'patternProperties':
        {r'\w[\w-]*': {'anyOf': [{'type': 'string'}, {'type': 'number'}]}}
}

definition = {
    'type': 'object',
    'default': {},
    'additionalProperties': False,
    'properties': {
        'set': dictionary_of_strings_or_num,
        'unset': array_of_strings_or_num,
        'prepend_path': dictionary_of_strings_or_num,
        'append_path': dictionary_of_strings_or_num,
        'remove_path': dictionary_of_strings_or_num
    }
}


def parse(config_obj):
    """Returns an EnvironmentModifications object containing the modifications
    parsed from input.

    Args:
        config_obj: a configuration dictionary conforming to the
            schema definition for environment modifications
    """
    import sys

    import spack.util.environment as ev
    if sys.version_info >= (3, 5):
        from collections.abc import Sequence  # novm
    else:
        from collections import Sequence  # novm

    env = ev.EnvironmentModifications()
    for command, variable in config_obj.items():
        # Distinguish between commands that take only a name as argument
        # (e.g. unset) and commands that take a name and a value.
        if isinstance(variable, Sequence):
            for name in variable:
                getattr(env, command)(name)
        else:
            for name, value in variable.items():
                getattr(env, command)(name, value)

    return env
