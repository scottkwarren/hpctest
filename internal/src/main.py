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

global tester
tester = HPCTest()      # must come early b/c initializes paths in common.*




def main():
        
    args = parseCommandLine()    
    return execute(args)


def parseCommandLine():
    # see https://docs.python.org/2/howto/argparse.html
    
    import argparse
    from os.path import join
    import common
    global tester
    
    # default values
    workpath = join(common.homepath, "work")
    
    # parsers
    parser = argparse.ArgumentParser(prog="hpctest")
    subparsers = parser.add_subparsers(dest="subcommand")

    # info ...

    # settings ...
    
    
    # -------------------------------------------------------------------------------------------------------
    # hpctest run [tspec | --tests tspec] [--configs cspec] [--hpctoolkits cspec] [--profile cspec] [--study study] <options>
    # -------------------------------------------------------------------------------------------------------
    runParser = subparsers.add_parser("run", help="run a set of tests on each of a set of cofigurations")
    runParser.add_argument("tests_arg",     nargs="?", type=str,  default="default",  help="testspec for the set of test cases to be run")
    runParser.add_argument("--tests",            "-t", type=str,  default="default",  help="testspec for the set of build configs on which to test")
    runParser.add_argument("--configs",          "-c", type=str,  default="default",  help="buildspec for the set of build configs on which to test")
    runParser.add_argument("--hpctoolkits",      "-H", type=str,  default="default",  help="paths to hpctoolkit instances with which to test")
    runParser.add_argument("--profile",          "-p", type=str,  default="default",  help="profiling parameters passed to hpctoolkit tools")
    runParser.add_argument("--study",            "-s", type=str,  default="default",  help="where to make study directory for this study")
##  runParser.add_argument("--numrepeats",       "-n", type=int,  default=1,          help="number of times to repeat each test run")
    runParser.add_argument("--report",           "-r", type=str,  default="default",  help="details of report to be produced")
    runParser.add_argument("--sort",             "-S", type=str,  default="default",  help="sequence of dimensions to sort report by")
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
    # hpctest _miniapps <options>
    # -------------------------------------------------------------------------------------------------------
    miniappsParser = subparsers.add_parser("miniapps", help="find all builtin miniapp packages and add test cases for them to tests/miniapp")
    _addOptionArgs(miniappsParser)

    # parse the command line
    args = parser.parse_args()
    if args.options is None: args.options = {}          # can argparse do this automagically?
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
    from common import options, errormsg

    if args.subcommand == "run":
        
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
        if args.configs != "default":
            dims["configs"] = args.configs
            del args.configs
        if args.hpctoolkits != "default":
            dims["hpctoolkits"] = args.hpctoolkits
            del args.hpctoolkits
        if args.profile != "default":                                                               # TODO: finish rework of 'hpctoolkitparams' into three args
            dims["hpctoolkitparams"] = args.profile.replace("_", "-").replace(".", " ")    # undo the workaround for argparse fail on quoted args
            del args.profile
        studyPath = args.study if args.study != "default" else None; del args.study
        numrepeats = 1  ## args.numrepeats
        otherargs  = args
        reportspec = args.report if args.report != "default" else "all"
        sortKeys   = [ key.strip() for key in (args.sort).split(",") ] if args.sort != "default" else []
        tester.run(dims, args, numrepeats, reportspec, sortKeys, studyPath)
        
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
    
    
    elif args.subcommand == "miniapps":
        
            tester.miniapps()
            
            
    else:
        
        fatalmsg("in main.execute, unexpected subcommand name")
    




if __name__ == "__main__": main()



