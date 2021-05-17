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


# manually maintained version id for hpctest
version = "1.0b4"

# magic cookie shielding 'hpctest _runOne' from civilians
magic_cookie = "Arma virumque cano Troiae qui primus ab oris"


# shared variables, set in HPCTest at startup
subcommand           = ""       # name of subcommand being executed
options              = []       # list of options parsed from command line
numErrors            = 0        # count of errors in this test run
homepath             = None     # path to this HPCTest installation
own_spack_home       = None     # path to private Spack's install directory
own_spack_module_dir = None     # path to private Spack's top-level module
ext_spack_home       = None     # path to external Spack's install directory if any -- can be None (TODO)
ext_spack_module_dir = None     # path to external Spack's top-level module, if any -- can be None (TODO)
hpctk_default        = None     # path to default installation of HPToolkit for use in profiling
testspath            = None     # path to this HPCTest's test directory
repopath             = None     # path to this HPCTest's repo for test packages
workpath             = None     # path to this HPCTest's arena for studies
logger               = None     # used to write test results (TODO)


# Math

def percent(a, b):
    
    if (a is None or a == "NA") or (b is None or b == "NA" or b == 0):
        formatted = " ---- "
    else:
        p = (float(a) / float(b)) * 100.0
        formatted = "  0   " if a == 0 else "< 0.1%" if p < 0.1  else "< 1  %" if p < 1.0 else "{:>5.1f}%".format(p)
        
    return formatted


def percentDelta(a, b):
    
    return percent(a-b, b)


# Options
  
def optionsArgString(options=None):
    
    import common
    if not options: options = common.options
    
    optString = ""
    if "quiet"      in options:    optString += " --quiet"
    if "verbose"    in options:    optString += " --verbose"
    if "debug"      in options:    optString += " --debug"
    if "force"      in options:    optString += " --force"
    if "traceback"  in options:    optString += " --traceback"
    
    return optString


def is_path_valid(path):

    import errno, os

    try:
        
        if not isinstance(path, str) or not path:
            return False

        root = os.path.sep

        # check whether each path component split from this path is valid
        for part in path.split(os.path.sep):
            try:
                os.lstat(root + part)
            except OSError as e:
                if e.errno in {errno.ENAMETOOLONG, errno.ERANGE}: # ERANGE if SunOS or *BSD
                    return False
    
    except TypeError as e:  # probably an embedded NUL character
        return False
    else:
        return True
    
    
def verboseOption():
    
    from common import options
    return " --verbose " if "verbose" in options else ""


# Message output

def infomsg(message):
    
    print message


def verbosemsg(message):
    
    if "verbose" in options:
        infomsg(message)


def debugmsg(message, always=False):
    
    if always or "debug" in options:
          infomsg(">>> " + message)


def warnmsg(message):
    
    infomsg("warning: " + message)


def errormsg(message):
    
    import sys
    import traceback
    
    global numErrors
    numErrors = numErrors + 1
    
    infomsg("error: " + message)
    if "traceback" in options or "debug" in options:
        traceback.print_stack()

def fatalmsg(message):
    
    import inspect, traceback

    info = inspect.getframeinfo(inspect.currentframe().f_back)
    infomsg("FATAL ERROR: {}\n"
            "             at {}:{}".format(message, info.filename, info.lineno))
    raise SystemExit
    
    
def assertmsg(predicate, message):
    
    if not predicate: fatalmsg(message)


def notimplemented(what):
    
    fatalmsg(what + " is not implemented")


def subclassResponsibility(cls, method):
    
    fatalmsg("{}.{} should be overridden by each subclass but was not".format(cls, method))


def mustNotCall(whatClass, whatMethod, reason):
    
    fatalmsg("{}.{} must not be called because {}".format(whatClass, whatMethod, reason))
    

def sepmsg(long=False):
    
    if type(long) is int:
        num = long
    else:
        num = (2 if long else 1) * 35
    infomsg("-" * num)


# String conveniences

def truncate(s, n):
    
    n = max(n,3)
    return (s[:n-3] + '...') if len(s) > n else s


def escape(s):

    return s.replace('\\', '\\\\')  \
            .replace("'", "\\'")    \
            .replace('"', '\\"')
    

# Stack traceback

def traceback():
    
    import traceback
    traceback.print_exc(limit=1000)


# Prompted input

def yesno(prompt, cancelmsg):
    
    reply = raw_input(prompt + " (y/n)?")
    ok = len(reply) > 0 and (reply[0] == "y" or reply[0] == "Y")
    if not ok: infomsg(cancelmsg)
    return ok


# list of values specified in yaml by a list-or-scalar expression

def noneOrMore(x):
    
    return x if type(x) is list else [x] if x is not None else []


# context manager for timing

class ElapsedTimer(object):
        
    def __init__(self, verbose=False):
        
        import time
        self.secs  = 0.0        # works around mystery bug where < __exit__ not called > => "unexpected error AttributeError ('ElapsedTimer' object has no attribute 'secs')"

    def __enter__(self):
        
        import time
        self.start = time.time()
        return self

    def __exit__(self, *args):
        
        import time
        self.secs += time.time() - self.start


# Finding executables on $PATH

def whichDir(exename):
    
    import os
    from os.path import dirname
    from util.which import which
    
    try:
        return dirname( which(exename) )
    except:
        return None


# Keypath access to dict-like objects    

def getValueAtKeypath(dictionary, keypath, default=None):
    
    keyList = keypath.split(".") if type(keypath) is str else keypath
    return _findValueAtKeypath(dictionary, keyList, None, False, default)


def setValueAtKeypath(dictionary, keypath, value):
    
    # decompose keypath into (adjusted) list of keys
    if type(keypath) is str: keypath = keypath.split(".")
    keyList  = keypath[:-1]    # path to object into which 'value' will be stored
    keyAfter = keypath[-1]     # key at which 'value' will be stored
    
    # find where to store 'value' and do so
    ob = _findValueAtKeypath(dictionary, keyList, keyAfter, True, None)
    ob[keyAfter] = value


def _findValueAtKeypath(dictionary, keyList, keyAfter, autoExtend, default):

    from collections import OrderedDict
    from common import fatalmsg

    def isCompatible(key, collection):
        ktype, ctype = type(key), type(collection)
        if ktype is str:
            return ctype is dict or ctype is OrderedDict
        elif ktype is int:
            return ctype is list
        else:
            fatalmsg("common.findValueForPath.isCompatible: invalid key type ({})".format(ktype))
    
    def collectionForKey(key):
        keytype = type(key)
        if keytype is str:
            return OrderedDict()
        elif keytype is int:
            return list()
        else:
            fatalmsg("common.findValueForPath.collectionForKey: invalid key type ({})".format(ktype))

    # descend into 'dictionary' using keys, possibly adding new dicts or lists as needed
    ob = dictionary
    for k, key in enumerate(keyList):
        if isCompatible(key, ob):
            if key not in ob:
                if autoExtend:
                    nextkey = keyList[k+1] if k+1 < len(keyList) else keyAfter
                    ob[key] = collectionForKey(nextkey)
                else:
                    ob = default
                    break
            ob = ob[key]
        else:
            ob = default
            break
            
    return ob
    

# Custom exceptions

class HPCTestError(Exception):
    """Superclass of all custom exceptions in HPCTest"""
    
    def __init__(self, message, errno=None):
        self.message = message
        self.errno  = errno
        
    def __str__(self):
        errno_str = " ({})".format(self.errno) if self.errno else ""
        return self.message + errno_str


class BadTestDescription(HPCTestError):
    pass

class BadBuildSpec(HPCTestError):
    pass

class PrepareFailed(HPCTestError):
    pass

class BuildFailed(HPCTestError):
    pass

class ExecuteFailed(HPCTestError):
    pass

class CheckFailed(HPCTestError):
    pass

class BadStudyPath(HPCTestError):
    pass



