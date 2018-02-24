################################################################################
#                                                                              #
#  common.py                                                                   #
#  storage for stuff shared by all modules, e.g. cmd line, debug, etc          #
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




# Shared variables, set in HPCTest at startup

options              = None     # list of options parsed from command line
numErrors            = 0        # count of errors in this test run
homepath             = None     # path to this HPCTest installation
ext_spack_home       = None     # path to external Spack's directory if any -- can be None
own_spack_home       = None     # path to private Spack's directory
own_spack_module_dir = None     # path to dir containing private Spack's top level module
workpath             = None     # path to this HPCTest's arena for orkspaces
logger               = None     # used to write test results -- TODO


# Message output

def infomsg(message):
    
    print message


def verbosemsg(message):
    
    if "verbose" in options:
        infomsg(message)


def debugmsg(message, always=False):
    
    if always or "debug" in options:
          infomsg(">>> " + message)


def errormsg(message):
    
    import traceback
    
    global numErrors
    numErrors = numErrors + 1
    
    infomsg("error: " + message)
    if "traceback" in options or "debug" in options:
        traceback.print_exc()


def fatalmsg(message):
    
    import inspect, traceback

    info = inspect.getframeinfo( inspect.currentframe().f_back )
    infomsg("FATAL ERROR: at {}:{}, ".format(info.filename, info.lineno) + message)
    raise SystemExit
    
    
def assertmsg(predicate, message):
    
    if not predicate: fatalmsg(message)


def notimplemented(what):
    
    fatalmsg(what + " is not implemented")


def sepmsg(long=False):
    
    infomsg("-----------------------------------" * (2 if long else 1))


# stack traceback

def traceback():
    
    import traceback
    traceback.print_exc(limit=1000)


# Prompted input

def yesno(prompt):
    
    reply = raw_input(prompt + " (y/n)?")
    return len(reply) > 0 and (reply[0] == "y" or reply[0] == "Y")


# Custom exceptions

class HPCTestError(Exception):
    pass

class BadTestDescription(HPCTestError):
    pass

class PrepareFailed(HPCTestError):
    pass

class BuildFailed(HPCTestError):
    pass

class ExecuteFailed(HPCTestError):
    pass

class CheckFailed(HPCTestError):
    pass

class BadWorkspacePath(HPCTestError):
    pass


# Reading hpctest.yaml files

def readYamlforTest(testDir):

    from os.path import join, basename
    from spackle import readYamlFile
    from common import BadTestDescription
        

    # read yaml file
    yaml, error = readYamlFile( join(testDir, "hpctest.yaml") )
    if error:
        raise BadTestDescription(error)

    # validate and apply defaults
    if not yaml.get("info"):
        yaml["info"] = {}
    if not yaml.get("info").get("name"):
        yaml["info"]["name"] = basename(testDir)
    # TODO...

    return yaml



