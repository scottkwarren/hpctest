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




#==================#
# Shared variables #
#==================#

# list of options parsed from command line
options = None

# count of errors in this test run
numErrors = 0

# logger used to write test results
####log = xxx    # TODO


#================#
# Message output #
#================#

def infomsg(message):
    print message

def verbosemsg(message):
    if "verbose" in options:
        print message

def errormsg(message):
    global numErrors
    numErrors = numErrors + 1
    infomsg("error: " + message)

def fatalmsg(message):
    global numErrors
    numErrors = numErrors + 1
    infomsg("FATAL ERROR:" + message)

def debugmsg(message, always=False):
    if always or "debug" in options:
          infomsg(">>> " + message)


#===================#
# Custom exceptions #
#===================#

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






