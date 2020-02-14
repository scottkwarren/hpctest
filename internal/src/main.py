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

global HPCTestOb
HPCTestOb = None




def main():
    
    import sys
    import common
    from common import debugmsg, errormsg
    from help import usage_message, help_message, optionNames
    from util.docopt import docopt, DocoptExit
            
    # parse the command line and execute it if valid
    try:
        args = docopt(doc=help_message, help=False)
        common.args = args
        common.options = { key[2:] : args[key] for key in args if key in optionNames and args[key] }
        debugmsg("main's argv = {}".format(sys.argv))
        debugmsg("parsed args = {}".format(args))    # requires 'common.options' to be set
        return execute(args)
    except DocoptExit as d:
        print usage_message + "\n" + "For more information use '--help'." + "\n"


def execute(args):
    # perform the requested operation by calling methods of HPCTest
    # TODO: figure out how to dispatch on subcommand so can implement 'hpctest clean'

    global HPCTestObm
    from collections import OrderedDict
    from os.path import join
    from common import options, errormsg, fatalmsg, version
    from help import help_message

    HPCTestOb = HPCTest()      # must come early b/c initializes paths in common.*

    if args["init"]:
        
        HPCTestOb.init()
        
    elif args["run"] or args["debug"]:
        
        dims = OrderedDict()
        if args["TESTS"]:
            dims["tests"] = args["TESTS"]
        if args["--tests"]:
            if "tests" in dims:
                errormsg("'--tests' cannot be combined with <tests> positional argument (ignored).")
            else:
                dims["tests"] = args["--tests"]
        if "tests" not in dims: dims["tests"] = "all"
        if args["--build"]:
            dims["build"] = args["--build"]
        if args["--hpctoolkit"]:
            dims["hpctoolkit"] = args["--hpctoolkit"]
        if args["--profile"]:                                             # TODO: finish rework of 'profile' into three args
            dims["profile"] = args["--profile"].replace("_", "-").replace(".", " ")    # TODO: REMOVE THIS LEGACY PROCESSING
        studyPath = args["--study"]
        numrepeats = 1  ## args["--numrepeats"]
        reportspec = args["--report"] if args["--report"] else "all"
        sortKeys   = [ key.strip() for key in (args["--sort"]).split(",") ] if args["--sort"] else []
        wantBatch  = args["--batch"] or args["--background"]
        HPCTestOb.run(dims, numrepeats, reportspec, sortKeys, studyPath, wantBatch)
        
    elif args["report"]:
        
        studyPath  = args["--study"]
        whichspec  = args["--which"] if args["--which"] else "all" 
        sortKeys   = [ key.strip() for key in (args["--sort"]).split(",") ] if args["--sort"] else []
        HPCTestOb.report(studyPath, whichspec, sortKeys)
        
    elif args["clean"]:    
        
        s = args["--studies"]
        b = args["--built"]
        d = args["--dependencies"]
        
        if s or b or d:
            if args["--all"]:
                infomsg("option '--all' may not be combined with other options, so is ignored")
        elif args["--all"]:
            s = True
            b = True
            d = True
        else:
            # default if no options
            s = True
            
        HPCTestOb.clean(s, b, d)

        
    elif args["spack"]:
        
        HPCTestOb.spack(" ".join(args["COMMAND"]))
    
        
    elif args["selftest"]:
        
        if args["TESTS"]:
            testspec = args["TESTS"]
        if args["--tests"]:
            if args["TESTS"]:
                errormsg("'--tests' cannot be combined with <tests> positional argument (ignored).")
            else:
                testspec = args["--tests"]
        studyPath = args["--study"]
        reportspec = args["--report"] if args["--report"] else "all"
        HPCTestOb.selftest(testspec, reportspec, studyPath)
    
    elif args["--help"]:
        
            print help_message
            
    
    elif args["--version"]:
        
            print version
            
    
    elif args["_miniapps"]:
        
            HPCTestOb.miniapps()
    
        
    elif args["_runOne"]:
        
        HPCTestOb._runOne(args["ENCODED_ARGS"])
            
            
    else:
        
        errormsg("in main.execute, unexpected subcommand name")
    




if __name__ == "__main__": main()



