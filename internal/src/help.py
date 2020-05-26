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
#       (ie no leading spaces before 'Usage:' et al)


usage_message = \
                \
"""
Usage:
  hpctest init
  hpctest (build | run | debug) [options] ( all | [TESTSPEC...] )
          [--build CONFIGSPEC]
          [--hpctoolkit PATHSPEC]
          [--profile PROFILESPEC]
          [--study PATH]
          [--report REPORTSPEC]
          [--sort SORTSPEC]
          [--background] [--foreground] [--batch] [--immediate]
  hpctest report [options] [STUDYSPEC]
          [--which WHICHSPEC]
          [--report REPORTSPEC]
          [--sort SORTSPEC]
  hpctest clean [options]
          [--studies]
          [--built]
          [--dependencies]
          [--all]
  hpctest spack [options] COMMAND ...
  hpctest selftest [options] ( all | [TESTSPEC...] ) [--study PATH]
  hpctest _miniapps
  hpctest _runOne [options] ENCODED_ARGS
  hpctest (--help | --version)
"""


# The '{}' below must appear at the end of line to avoid extra newline in 'help_message'

# Example description:
#     HPCToolkit is an integrated suite of tools for measurement and analysis
#     of program performance on computers ranging from multicore desktop
#     systems to the nation's largest supercomputers. By using statistical
#     sampling of timers and hardware performance counters, HPCToolkit
#     collects accurate measurements of a program's work, resource
#     consumption, and inefficiency and attributes them to the full calling
#     context in which they occur.

_template = \
            \
"""
HPCTest:

Conduct a study using a "testing matrix" of alternative test conditions. A test run is carried out
for each matrix element using that element's parameters, and the results for all test runs are
saved to a "study directory" for subsequent inspection. Each matrix dimension specifies a set of
alternative values for one testing parameter, such as the test case to run or Spack configuration
to build it with; thus each matrix element is a tuple of parameters for a single test run.
  
"""                \
+ usage_message +  \
"""
Options:
  -v, --verbose              xxx.
  -D, --debug                xxx.
  -x, --force                xxx.
  -x, --nochecksum           xxx.
  -x, --quiet                xxx.
  -x, --traceback            xxx.{}
  
Arguments:
  COMMAND                    xxx. (Caution about [options] in Spack command: quote the command.)
  CONFIGSPEC                 a Spack spec minus the package name and caret (eg gcc@4.7).
  PATH                       xxx.
  PATHSPEC                   xxx.
  PROFILESPEC                a sequence of profiling arguments to 'hpcrun'.
  REPORTSPEC                 xxx.
  SORTSPEC                   xxx.
  TESTSPEC                   xxx.
  WHICHSPEC                  xxx.

Examples:
  hpctest run all
  hpctest run app/amgmk
  hpctest run app/amgmk --build %gcc@4.4.7,%gcc@4.8.5
  hpctest run app/AMG2006 --build  %gcc^mpich@3.1.4
  hpctest run "unit-test/cpp_threads,app/amgmk" --build "%gcc,%clang"
  hpctest run "unit-test/cpp_threads,app/amgmk" --build "%gcc@4.4.7,%gcc@4.8.5" --profile "REALTIME@10000,REALTIME@100"
  
"""


_hidden_options = \
                  \
"""
  -t, --tests TESTSPEC       Add a matrix dimension with the specified set of tests as alternatives.
                             Each test's executable will be executed as the test case for some runs of the study.
  -b, --build CONFIGSPEC     Add a matrix dimension with the specified set of build configurations as alternatives;
                             each configuration is used to build the test executable for some runs of the study.
  -k, --hpctoolkit PATHSPEC  Add a matrix dimension with the specified set of paths as alternatives; each path
                             points to an HPCToolkit installation's 'install/bin' directory and is used to profile
                             the test executable for some runs of the study.
  -p, --profile PROFILESPEC  Add a matrix dimension with the specified set of profile strings as alternatives;
                             each string is used to profile the test executable for some runs of the study.
  -o, --study PATH           xxx.
  -w, --which WHICHSPEC      xxx.
  -r, --report REPORTSPEC    xxx [Default: all].
  -S, --sort SORTSPEC        xxx.
  -s, --studies              xxx.
  -B, --built                xxx.
  -d, --dependencies         xxx.
"""


help_message = _template.format("")
doc_message  = _template.format(_hidden_options)


optionNames = \
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




