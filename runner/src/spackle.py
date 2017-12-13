################################################################################
#                                                                              #
#  spackle.py                                                                  #
#  thin wrapper around private Spack to expose operations we need              #
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




def do(cmdstring):
    
    import os, common
    os.system(common.own_spack_home + "/bin/spack " + cmdstring)    # cmdstring contents must be shell-escaped by caller


def extDo(cmdstring):
    
    import os, common
    os.system(common.ext_spack_home + "/bin/spack " + cmdstring)    # cmdstring contents must be shell-escaped by caller


def loadYamlFile(path):
    
    import os, spack, yaml                                          # 'yaml from lib/spack/external via sys.path adjustment in HPCTest.__init__
    from common import infomsg, debugmsg, errormsg

    debugmsg("loading yaml file at {}".format(path))
        
    try:
        
        with open(path, 'r') as f:
            try:
                object, msg = yaml.load(f), None
            except:
                object, msg = None, "file has syntax errors and cannot be used"
            
    except Exception as e:
        if isinstance(e, OSError) and e.errno == errno.EEXIST:
            object, msg = None, "file is missing"
        else:
            object, msg = None, "file cannot be opened: (error {0}, {1})".format(e.errno, e.strerror)
    
    debugmsg("...finished loading yaml file with result object {} and msg {}".format(object, repr(msg)))
    
    return object, msg


# Executing a command with error checkings

def execute(cmd, *args, **kwargs):
    
    from spack.util.executable import Executable, ExecuteFailed

    oldwd = os.getcwd()
    newwd = kwargs.get('cwd', None)
    exe   = Executable(cmd)
    
    try:
        if newwd: os.chdir(newwd)
        exe(self, args, kwargs)
    except:
        errormsg("{} command failed: {}", exe.name(), sys.exc_info()[0])
    finally:
        if newwd: os.chdir(oldwd)






    
    