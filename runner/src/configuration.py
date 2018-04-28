################################################################################
#                                                                              #
#  configuration.py                                                            #
#  layered storage for HPCTest config params                                   #
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




# current configuration as an OrderedDict
currentConfig = None


def initConfig():
    
    from os.path import join, isfile
    import common
    from common import homepath, errormsg
    from spackle import readYamlFile, writeYamlFile
    global currentConfig
    
    # compute filesys locations of layered config files from most global to most local
    builtin = join(homepath, "runner", "src", "config-builtin.yaml")
    user    = join("~", ".hpctest", "config.yaml")
    install = join(homepath, "config.yaml")
    configFileLocations = [ builtin, user, install ]
    
    # gather config info from layered yaml files w/ most local == highest priority
    currentConfig = {}
    for path in configFileLocations:
        if isfile(path):
            config, msg = readYamlFile(path)
            if msg:
                errormsg("ignoring invalid config file {}".format(path))
            else:
                _overrideDict(currentConfig, config)


def get(keypath, default=None):
    
    global currentConfig

    keys = keypath.split(".")
    
    value = currentConfig
    for k in keys:
        if value:
            try:
                value = value[k]
            except:
                value = None

    return value if value else default


def set(key, value):
    
    from common import notimplemented
    notimplemented("hpctest.configuration.set")


def _overrideDict(dict1, dict2):

    from collections import Mapping, MutableMapping

    for key, value2 in dict2.iteritems():
        if value2 != None:
            if key in dict1 and dict1[key]:
                value1 = dict1[key]
                if isinstance(value1, MutableMapping) and isinstance(value2, Mapping):  ## TODO: FIX CASE "key in both, V1 is scalar, V2 is dict & vv"
                    _overrideDict(value1, value2)
                else:
                    dict1[key] = value2
            else:
                dict1[key] = value2






