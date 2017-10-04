################################################################################
#                                                                              #
#  main.py                                                                     #
#  main program, converts Unix-style command line to HPCTest method calls      #
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
#  Copyright ((c)) 2002-2017, Rice University                                  #
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


from hpctest import HPCTest

import argparse
from sys import path

global tester
tester = HPCTest()




def main():
    
    args = parseCommandLine()    
    return execute(args)


def parseCommandLine():
    # see https://docs.python.org/2/howto/argparse.html
    
    import common   # 'from common import options, debugmsg' fails: 'options = ...' here does not set 'common.options'
    global tester
    
    # parsers
    parser = argparse.ArgumentParser(prog="hpctest")
    subparsers = parser.add_subparsers()

    # info ...

    # settings ...
    
    # hpctest run [tspec] [--tests tspec] [--configs cspec] [--dir workdir] <options>
    runParser = subparsers.add_parser("run", help="run a set of tests on each of a set of cofigurations")

    # ... tests
    testGroup = runParser.add_mutually_exclusive_group()
    testGroup.add_argument("tests", nargs="?", type=str, default="all", help="test-spec for the set of test cases to be run")
    testGroup.add_argument("--tests",   "-t",  type=str, default="all", help="test-spec for the set of test cases to be run")

    # ... configs
    runParser.add_argument("--configs", "-c",  type=str, default="default", help="build-spec for the set of build configs on which to test")

    # ... workdir
    runParser.add_argument("--dir",     "-d",  type=str, default=tester.homepath, help="working directory in which to run the set of tests")
    
    # ... options
    parser.add_argument("--int", dest="options", action="append_const", const=int)
    runParser.add_argument("--quiet",   "-q", dest="options", action="append_const", const="quiet",   help="run silently")
    runParser.add_argument("--verbose", "-v", dest="options", action="append_const", const="verbose", help="print additional details as testing is performed")
    runParser.add_argument("--debug",   "-D", dest="options", action="append_const", const="debug",   help="print debugging information as testing is performed")

    # parse the command line
    args = parser.parse_args()
    if args.options is None: args.options = {}          # can argparse do this automagically?
    common.options = args.options
    common.debugmsg("parsed args = {}".format(args))  # requires 'common.options' to be set

    return args


def execute(args):
    # perform the requested operation by calling methods of HPCTest
    
    global tester
    return tester.run(args.tests, args.configs, args.dir)




if __name__ == "__main__": main()



