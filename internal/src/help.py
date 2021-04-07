################################################################################
#                                                                              #
#  help.py                                                                     #
#  Help message text in Docopt format, used by 'main' to implement '--help'    #
#                                                                              #
#  (see https://github.com/docopt/docopt#readme)                               #
#                                                                              #
#  $HeadURL$                                                                   #
#  $Id$                                                                        #
#                                                                              #
#  --------------------------------------------------------------------------- #
#  Part of HPCToolkit (hpctoolkit.org)                                         #
#                                                                              #
#  Information about sources of support for research and development of        #
#  HPCToolkit is at "hpctoolkit.org" and in "README.Acknowledgments".          #
#  --------------------------------------------------------------------------- #
#                                                                              #
#  Copyright ((c)) 2002-2020, Rice University                                  #
#  All rights reserved.                                                        #
#                                                                              #
#  Redistribution and use in source and binary forms, with or without          #
#  modification, are permitted provided that the following conditions are      #
#  met:                                                                        #
#                                                                              #
#  * Redistributions of source code must retain the above copyright            #
#    notice, this list of conditions and the following disclaimer.             #
#                                                                              #
#  * Redistributions in binary form must reproduce the above copyright         #
#    notice, this list of conditions and the following disclaimer in the       #
#    documentation and/or other materials provided with the distribution.      #
#                                                                              #
#  * Neither the name of Rice University (RICE) nor the names of its           #
#    contributors may be used to endorse or promote products derived from      #
#    this software without specific prior written permission.                  #
#                                                                              #
#  This software is provided by RICE and contributors "as is" and any          #
#  express or implied warranties, including, but not limited to, the           #
#  implied warranties of merchantability and fitness for a particular          #
#  purpose are disclaimed. In no event shall RICE or contributors be           #
#  liable for any direct, indirect, incidental, special, exemplary, or         #
#  consequential damages (including, but not limited to, procurement of        #
#  substitute goods or services; loss of use, data, or profits; or             #
#  business interruption) however caused and on any theory of liability,       #
#  whether in contract, strict liability, or tort (including negligence        #
#  or otherwise) arising in any way out of the use of this software, even      #
#  if advised of the possibility of such damage.                               #
#                                                                              #
################################################################################


# This string serves two purposes:
# it defines and implements the 'hpctest' command line syntax ( via 'docopt'), and
# it provides the help message printed by 'hpctest --help' and on cmd line errors.

# NOTE: the docstring must be at the left margin for 'docopt' to interpret it correctly
#       (ie no leading spaces before 'Usage:')


#==============#
# USAGE STRING #
#==============#

_usage = \
         \
"""
Usage:
  hpctest init [options] [--spack PATH]
  hpctest (build | run | debug) [options] (all | [TESTSPEC...])
          [--test TESTSPEC]
          [--build BUILDSPEC]
          [--hpctoolkit HPCTKSPEC]
          [--profile PROFILESPEC]
          [--study PATH]
          [--report REPORTSPEC]
          [--sort SORTSPEC]
          [--background] [--foreground] [--batch] [--immediate]
  hpctest report [options] [PATH]
          [--which WHICHSPEC]
          [--sort SORTSPEC]
  hpctest clean [options]
          [--studies]
          [--built]
          [--dependencies]
          [--all]
  hpctest spack [options] SPACKCMD ...
  hpctest selftest [options] ( all | [TESTSPEC...] ) [--study PATH]
  hpctest _runOne [options] ENCODED_ARGS
  hpctest (--help | --version)
  
"""


#===============#
# HELP TEMPLATE #
#===============#

# Example description:
#     HPCToolkit is an integrated suite of tools for measurement and analysis
#     of program performance on computers ranging from multicore desktop
#     systems to the nation's largest supercomputers. By using statistical
#     sampling of timers and hardware performance counters, HPCToolkit
#     collects accurate measurements of a program's work, resource
#     consumption, and inefficiency and attributes them to the full calling
#     context in which they occur.

_help = \
        \
"""
HPCTest is a tool for flexible automatic configuration testing of the HPCToolkit
suite of tools. Using a collection of builtin test cases and concise
specifications given on its command line, HPCTest conducts a study by performing
test runs over a "testing matrix" of configurations, gathering and organizing
test measurements, and printing a report summarizing the results.
All test artifacts are saved in a "study directory" for later inspection.

A testing matrix is specified on the command line by a sequence of "dimension
spec" options. Each dimension spec defines a set of alternative values for one
test condition (a dimension), such as which test case to run or which Spack
configuration to build with. The testing matrix is the cross product of those
sets. Each matrix element is then a tuple of test condition values
(a "configuration") applicable to any individual test run. A dimension spec is
an expression in dimension-dependent notation specifying a set of values either
implicitly or explicitly.

For instance, '--test app/amg*' implicitly specifies a set of values for the
'test' condition (paths to tests) using shell "glob" path patterns, while
'--build %gcc@4.4.7,%gcc@4.8.5' explicitly specifies a set of values for the
'build' condition (build settings) using Spack configuration syntax. The other
dimension spec options are '--hpctoolkit' and '--profile' specifying hpctoolkit
installations and hpcrun profile settings respectively. Dimensions not specified
are given single dimension-dependent default values.

HPCTest accepts a number of subcommands on its command line. The 'run' subcommand
conducts a study using given dimension specs, while 'build' just builds the tests
and 'debug' runs each test in the debugger. The 'report' subcommand prints a
report from an existing study directory, and the 'clean' command removes unwanted
study directories, and several minor commands carry out utility operations.

Options: Informational
  -q, --quiet             Print as little as reasonable.
  -v, --verbose           Print additional informational messages.
  -D, --debug             Print debugging messages.
  -T, --traceback         Print a stack trace when an error occurs.

Options: Testing
  -t, --test TESTSPEC
            Add a dimension with the set TESTSPEC of tests as alternatives.
            Each element is a path to a test directory relative to hpctest/tests.
  -b, --build BUILDSPEC
            Add a dimension with the set BUILDSPEC of build settings as alternatives.
            Each element is a Spack spec minus package name, like %gcc@4.8.5.
  -k, --hpctoolkit HPCTKSPEC
            Add a dimension with the set HPCTKSPEC of paths as alternatives.
            Each element is a path to an HPCToolkit install/bin directory.
  -p, --profile PROFILESPEC
            Add a dimension with the set PROFILESPEC of profile options as
            alternatives. Each element is a colon-separated triple of options
            for hpcrun, hpcstruct, and hpcprof.
  -o, --study STUDYPATH
            If given, create the study directory at the specified path. Otherwise
            the default is to create it inside the hpctest/work directory.
  -V, --version
            Print this hpctest's version number.

Options: Reporting
  -w, --which WHICHSPEC
            Print only the specified subset of test results.
  -S, --sort SORTSPEC
            Print the test results sorted by each specified field in turn.

Options: Cleaning
  -s, --studies
            Remove all study directories from hpctest/work.
  -B, --built
            Remove all built test executables, not including their dependencies.
  -d, --dependencies
            Remove all built dependencies of all tests.
  -f, --force
            Don't ask for confirmation, just remove the specified objects.

Arguments:        All lists are comma separated.
  BUILDSPEC       list of Spack specs minus package names, eg '%gcc@4.4.7'
  HPCTKSPEC       list of paths with wildcards pointing to hpctoolkit/install dirs
  PROFILESPEC     list of colon-separated arguments to hpcrun:hpcstruct:hpcprof
  SORTSPEC        list of dimensions ('tests'/'build'/'profile'/'hpctoolkit')
  SPACKCMD        subcommand for Spack, eg 'install openmpi'
  STUDYPATH       path with wildcards, absolute or relative to hpctest/work
  TESTSPEC        list of paths with wildcards relative to hpctest/tests
  WHICHSPEC       one of 'all', 'pass', or 'fail'

Examples:

  hpctest run all
  hpctest run app/amgmk,app/lulesh, app/laghos
  hpctest run app/amg*, unit-test/*

  hpctest run all --build %gcc@4.4.7
  hpctest run all --build %clang^mpich@3.1.4
  hpctest run all --build "%gcc@4.4.7, %gcc@4.8.5, clang"

  hpctest run unit-test/*, app/amg*  \\
          --build "%gcc@4.4.7, %gcc@4.8.5"  \\
          --profile "REALTIME@10000, REALTIME@1000, REALTIME@100"  \\
          --study ~/mystudies/june/trial_12
  
  hpctest report --study study-2020-06-01--18-29-59 --which fail --sort build
  
  hpctest clean --all -f
  
"""


#=============#
# OPTION LIST #
#=============#

_optlist = \
    [
    '--background',
    '--batch',
    '--foreground',
    '--immediate',
    '--debug',
    "--force",
    '--help',
    "--nochecksum"
    "--quiet",
    "--traceback",
    '--verbose',
    ]


#======================#
# PUBLIC DEFINITIONSES #
#======================#

usage_message = _usage
help_message  = _usage + _help
option_list   = _optlist




