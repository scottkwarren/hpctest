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


#### TEMPORARY: ALL CODE INVOLVING 'numrepeats' IS STUBBED OUT FOR NOW


from hpctest import HPCTest


def main():
        
    args = parseCommandLine()    
    return execute(args)


def parseCommandLine():
    # see https://docs.python.org/2/howto/argparse.html
    
    import argparse
    from os.path import join
    import common
    global tester
    
    # parsers
    parser = argparse.ArgumentParser(prog="hpctest")
    subparsers = parser.add_subparsers(dest="subcommand")


    # -------------------------------------------------------------------------------------------------------
    # hpctest init
    # -------------------------------------------------------------------------------------------------------
    initParser = subparsers.add_parser("init", help="initialize HPCTest")
    _addOptionArgs(initParser)   # useless, but avoids special case in 'execute'
    
    # -------------------------------------------------------------------------------------------------------
    # hpctest run [tspec | --tests tspec] [--build cspec] [--hpctoolkit tkspec] [--profile pspec] [--study study] <options>
    # -------------------------------------------------------------------------------------------------------
    runParser = subparsers.add_parser("run", help="run a set of tests on each of a set of cofigurations")
    runParser.add_argument("tests_arg",     nargs="?", type=str,  default="default",  help="testspec for which test cases to run")
    runParser.add_argument("--tests",            "-t", type=str,  default="default",  help="testspec for which test cases to rum")
    runParser.add_argument("--build",            "-b", type=str,  default="default",  help="buildspec for which build configs on which to use")
    runParser.add_argument("--hpctoolkit",       "-k", type=str,  default="default",  help="paths to hpctoolkit instances to use")
    runParser.add_argument("--profile",          "-p", type=str,  default="default",  help="profiling parameters to pass to hpctoolkit tools")
    runParser.add_argument("--study",            "-s", type=str,  default="default",  help="where to put study directory for this study")
##  runParser.add_argument("--numrepeats",       "-n", type=int,  default=1,          help="number of times to repeat each test run")
    runParser.add_argument("--report",           "-r", type=str,  default="default",  help="details of report to print")
    runParser.add_argument("--sort",             "-S", type=str,  default="default",  help="sequence of dimensions to sort report by")
    runParser.add_argument("--background",       "-Z", type=str,  default="default",  help="run in the background")
    runParser.add_argument("--batch",            "-B", type=str,  default="default",  help="run as batch jobs")
    _addOptionArgs(runParser)

    # -------------------------------------------------------------------------------------------------------
    # hpctest report [--study study] [--which whichspec] [--sort sortspec] <options>
    # -------------------------------------------------------------------------------------------------------
    reportParser = subparsers.add_parser("report",                                    help="print report summarizing a study")
    reportParser.add_argument("--study",     "-s",     type=str,  default="default",  help="path to study directory to report on")
    reportParser.add_argument("--which",     "-w",     type=str,  default="default",  help="which test runs to report on")
    reportParser.add_argument("--sort",      "-S",     type=str,  default="default",  help="sequence of dimensions to sort report by")
    _addOptionArgs(reportParser)

    # -------------------------------------------------------------------------------------------------------
    # hpctest clean [ --all | [-s|--study  [study] ] [-t|-tests] [-d|--dependencies] ]   <options>
    # -------------------------------------------------------------------------------------------------------
    cleanParser = subparsers.add_parser("clean",                                      help="clean up by deleting unwanted testing byproducts")
    cleanParser.add_argument("--studies",      "-s",   type=str, nargs="?", const="<default>", help="delete study directories from workspace")
    cleanParser.add_argument("--tests",        "-t",   action="store_true",           help="uninstall built tests")
    cleanParser.add_argument("--dependencies", "-d",   action="store_true",           help="uninstall packages built to satisfy tests' dependencies")
    cleanParser.add_argument("--all",          "-a",   action="store_true",           help="clean studies, tests, and dependencies")
    _addOptionArgs(cleanParser)

    # -------------------------------------------------------------------------------------------------------
    # hpctest spack <cmd>
    # -------------------------------------------------------------------------------------------------------
    spackParser = subparsers.add_parser("spack", help="run a Spack command with hpctest's private Spack")
    spackParser.add_argument('spackcmd', nargs=argparse.REMAINDER)
    _addOptionArgs(spackParser)

    # -------------------------------------------------------------------------------------------------------
    # hpctest selftest <options>
    # -------------------------------------------------------------------------------------------------------
    selftestParser = subparsers.add_parser("selftest", help="run HPCTest's builtin self tests")
    selftestParser.add_argument("tests_arg", nargs="?", type=str, default="default",  help="testspec for which self tests to run")
    selftestParser.add_argument("--tests", "-t", type=str,  default="default",  help="testspec for which self tests to run")
    selftestParser.add_argument("--study", "-s", type=str,  default="default",  help="where to put study directory for this study")
    _addOptionArgs(selftestParser)

    # -------------------------------------------------------------------------------------------------------
    # hpctest _miniapps <options>
    # -------------------------------------------------------------------------------------------------------

#     miniappsParser = subparsers.add_parser("miniapps", help="find all builtin miniapp packages and add test cases for them to tests/miniapp")
#     _addOptionArgs(miniappsParser)

    # parse the command line
    args = parser.parse_args()
    if args.options is None: args.options = {}          # can argparse do this automagically?
    common.subcommand = args.subcommand
    common.options = args.options
    common.debugmsg("parsed args = {}".format(args))    # requires 'common.options' to be set

    return args


def _addOptionArgs(subparser):
    
    subparser.add_argument("--quiet",      "-q",  dest="options", action="append_const", const="quiet",      help="run silently")
    subparser.add_argument("--verbose",    "-v",  dest="options", action="append_const", const="verbose",    help="print additional details as testing is performed")
    subparser.add_argument("--debug",      "-D",  dest="options", action="append_const", const="debug",      help="print debugging information as testing is performed")
    subparser.add_argument("--force",      "-F",  dest="options", action="append_const", const="force",      help="do not ask for confirmation and ignore errors")
    subparser.add_argument("--traceback",  "-T",  dest="options", action="append_const", const="traceback",  help="print stack traces with error messages")
    subparser.add_argument("--nochecksum", "-C",  dest="options", action="append_const", const="nochecksum", help="ignore checksum of 'tests' directory tree")
    

def execute(args):
    # perform the requested operation by calling methods of HPCTest
    # TODO: figure out how to dispatch on subcommand so can implement 'hpctest clean'

    global tester
    from collections import OrderedDict
    from os.path import join
    from common import options, errormsg, fatalmsg

    tester = HPCTest()      # must come early b/c initializes paths in common.*

    if args.subcommand == "init":
        
        tester.init()
        
    elif args.subcommand == "run":
        
        dims = OrderedDict()
        if args.tests_arg != "default":
            dims["tests"] = args.tests_arg
            del args.tests_arg
        if args.tests != "default":
            if "tests" in dims:
                errormsg("'--tests' cannot be combined with <tests> positional argument (ignored).")
            else:
                dims["tests"] = args.tests
                del args.tests
        if args.build != "default":
            dims["build"] = args.build
            del args.build
        if args.hpctoolkit != "default":
            dims["hpctoolkit"] = args.hpctoolkit
            del args.hpctoolkit
        if args.profile != "default":                                             # TODO: finish rework of 'profile' into three args
            dims["profile"] = args.profile.replace("_", "-").replace(".", " ")    # undo the workaround for argparse fail on quoted args
            del args.profile
        studyPath = args.study if args.study != "default" else None; del args.study
        numrepeats = 1  ## args.numrepeats
        otherargs  = args
        reportspec = args.report if args.report != "default" else "all"
        sortKeys   = [ key.strip() for key in (args.sort).split(",") ] if args.sort != "default" else []
        wantBatch  = args.batch or args.background
        tester.run(dims, otherargs, numrepeats, reportspec, sortKeys, studyPath, wantBatch)
        
    elif args.subcommand == "report":
        
        studyPath  = args.study if args.study != "default" else None; del args.study
        whichspec  = args.which if args.which != "default" else "all" 
        sortKeys   = [ key.strip() for key in (args.sort).split(",") ] if args.sort != "default" else []
        tester.report(studyPath, whichspec, sortKeys)
        
    elif args.subcommand == "clean":    
        
        s = args.studies
        t = args.tests
        d = args.dependencies
        
        if s or t or d:
            if args.all:
                infomsg("option '--all' may not be combined with other options, so is ignored")
        elif args.all:
            s = "<default>"
            t = True
            d = True
        else:
            s = "<default>"
            
        tester.clean(s, t, d)

        
    elif args.subcommand == "spack":
        
        tester.spack(" ".join(args.spackcmd))
    
        
    elif args.subcommand == "selftest":
        
        if args.tests_arg != "default":
            testspec = args.tests_arg
            del args.tests_arg
        if args.tests != "default":
            if args.tests_arg != "default":
                errormsg("'--tests' cannot be combined with <tests> positional argument (ignored).")
            else:
                testspec = args.tests
                del args.tests
        studyPath = args.study if args.study != "default" else None; del args.study
        otherargs  = args
        reportspec = args.report if args.report != "default" else "all"
        tester.selftest(testspec, otherargs, reportspec, studyPath)
    
    elif args.subcommand == "miniapps":
        
            tester.miniapps()
            
            
    else:
        
        fatalmsg("in main.execute, unexpected subcommand name")
    




if __name__ == "__main__": main()



