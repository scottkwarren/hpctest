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
#  HPCToolkit is at 'hpctoolkit.org' and in 'README.Acknowledgments'.          #
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

import argparse
import os

from hpctest import HPCTest 
hpctest = HPCTest()




def main():
    args = parseCommandLine()
    return execute(args)


def parseCommandLine():
    # see https://docs.python.org/2/howto/argparse.html
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    
    # info ...

    # settings ...
    
    # run [tspec ] [--tests tspec] [--configs cspec] [--dir path] <options>
    runParser = subparsers.add_parser('run', help='run a set of tests on each of a set of cofigurations')
    group = runParser.add_mutually_exclusive_group()
    group.add_argument("tests", nargs='?', type=str, default="all", help="test-spec for the set of test cases to be run")
    group.add_argument("--tests", "-t", type=str, default="all", help="test-spec for the set of test cases to be run")
    runParser.add_argument("--configs", "-c", type=str, default="default", help="build-spec for the set of build configs on which to test")
    runParser.add_argument("--dir", "-d", type=str, default=os.getcwd(), help="working directory in which to run the set of tests")
    
    return parser.parse_args()


def execute(args):
    print args  # DEBUG
    # perform the requested operation by calliung methods of HPCTest
    hpctest.run(tests=args.tests, configs=args.configs, dir=args.dir)
    return 0




if __name__ == '__main__':
  main()



