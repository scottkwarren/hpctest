################################################################################
#                                                                              #
#  hpctest.py                                                                  #
#  top level class implementing functionality of HPCTest for programmatic use  #
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
##############################################################################


import os, shutil
import common   # 'from common import options, debugmsg' fails: 'options = ...' here does not set 'common.options'


class HPCTest():
    
    def __init__(self, homepath=None):
        
        if homepath is not None:
            self.homepath = os.environ["HPCTEST_HOME"] = homepath
        else:
            self.homepath = os.environ["HPCTEST_HOME"]   # can fail!


    def run(self, testSpec, configSpec, workpath):
        
        #from common import options, debugmsg
        from testspec   import TestSpec
        from configspec import ConfigSpec
        from workspace  import Workspace
        from iterate    import Iterate
        from report     import Report

        common.debugmsg("will run tests {} on configs {} in workspace {} with options {}"
                            .format(testSpec, configSpec, workpath, common.options))
        
        tests     = TestSpec(testSpec)
        configs   = ConfigSpec(configSpec)
        workspace = Workspace(workpath)
        
        status  = Iterate.doForAll(tests, configs, workspace)
        Report.printReport(workspace)
        
        return status


    def clean(self, workpath):
        
        common.debugmsg("cleaning work directory {}".format(workpath))
        
        for name in os.listdir(workpath):
            path = os.path.join(workpath, name)
            if name.startswith("workspace-") and os.path.isdir(path):
                shutil.rmtree(path, ignore_errors=True)

                
                

