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

import argparse, os

global tester
tester = HPCTest()




def main():
        
    args = parseCommandLine()    
    return execute(args)


def parseCommandLine():
    # see https://docs.python.org/2/howto/argparse.html
    
    from common import debugmsg
    import common   # 'from common import debugmsg' fails b/c 'options = ...' is treated as assignment to local, even with 'global options'
    global tester
    
    # default values
    workpath = os.path.join(tester.homepath, "work")
    
    # parsers
    parser = argparse.ArgumentParser(prog="hpctest")
    subparsers = parser.add_subparsers(dest="subcommand")

    # info ...

    # settings ...
    
    
    # ----------------------------------------------------------------------------------------
    # hpctest run [tspec] [--tests tspec] [--configs cspec] [--workspace workspace] <options>
    # ----------------------------------------------------------------------------------------
    runParser = subparsers.add_parser("run", help="run a set of tests on each of a set of cofigurations")

    # ... tests
    testGroup = runParser.add_mutually_exclusive_group()
    testGroup.add_argument("tests", nargs="?",   type=str, default="all", help="test-spec for the set of test cases to be run")
    testGroup.add_argument("--tests",     "-t",  type=str, default="all", help="test-spec for the set of test cases to be run")

    # ... configs
    runParser.add_argument("--configs",   "-c",  type=str, default="default", help="build-spec for the set of build configs on which to test")

    # ... workspace
    runParser.add_argument("--work",      "-w",  type=str, default=workpath, help="directory in which to create workspace for this run")
    
    # ... options
    runParser.add_argument("--quiet",     "-q",  dest="options", action="append_const", const="quiet",   help="run silently")
    runParser.add_argument("--verbose",   "-v",  dest="options", action="append_const", const="verbose", help="print additional details as testing is performed")
    runParser.add_argument("--debug",     "-D",  dest="options", action="append_const", const="debug",   help="print debugging information as testing is performed")


    # ----------------------------------------------------------------------------------------
    # hpctest clean [<workspaces>] <options>
    # ----------------------------------------------------------------------------------------
    cleanParser = subparsers.add_parser("clean", help="clean up by deleting unwanted workspaces")

    # ... workspaces
    workspacesGroup = cleanParser.add_mutually_exclusive_group()
    workspacesGroup.add_argument("work", nargs="?", type=str, default=workpath, help="path to workspace or dir-of-workspaces to be cleaned")
    workspacesGroup.add_argument("--work", "-w",    type=str, default=workpath, help="path to workspace or dir-of-workspaces to be cleaned")
    
    # ... options
    cleanParser.add_argument("--quiet",     "-q",  dest="options", action="append_const", const="quiet",   help="run silently")
    cleanParser.add_argument("--verbose",   "-v",  dest="options", action="append_const", const="verbose", help="print additional details as cleaning is performed")
    cleanParser.add_argument("--debug",     "-D",  dest="options", action="append_const", const="debug",   help="print debugging information as cleaning is performed")


    # parse the command line
    args = parser.parse_args()
    if args.options is None: args.options = {}          # can argparse do this automagically?
    common.options = args.options
    debugmsg("parsed args = {}".format(args))    # requires 'common.options' to be set

    return args


def execute(args):
    # perform the requested operation by calling methods of HPCTest
    # TODO: figure out how to dispatch on subcommand so can implement 'hpctest clean'

    global tester

    if args.subcommand == "run":
        return tester.run(args.tests, args.configs, args.work)
    elif args.subcommand == "clean":
        return tester.clean(args.work)
    else:
        fatalmsg("in main.execute, unexpected subcommand name")
    




if __name__ == "__main__": main()



