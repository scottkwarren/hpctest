################################################################################
#                                                                              #
#  run.py                                                                      #
#  run a single test case in a testdir workdirectory                            #
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


import os
from common  import options, infomsg, errormsg, debugmsg
from common  import BadTestDescription, PrepareFailed, BuildFailed, ExecuteFailed, CheckFailed
from spackle import loadYamlFile



class Run():
    
    def __init__(self, testdir, config, workspace):
        
        self.testdir   = testdir        # path to test case's directory
        self.config    = config         # Spack spec for desired build configuration
        self.workspace = workspace      # storage for collection of test work workdirs

        # set up for per-test sub-logging
        ####self.log = xxx    # TODO


    def run(self):
        
        infomsg("running test {} with config {}".format(self.testdir, self.config))
        
        try:
            
            testDesc = self.readTestDescription()
            (srcdir, builddir, rundir)  = self.prepareWorkDir(testDesc)
            self.buildTest(testDesc, srcdir, builddir)
            self.executeBuiltTest(testDesc, builddir, rundir)
            self.checkTestResults(testDesc, rundir)
            
        except BadTestDescription:
            errormsg("missing or invalid 'hpctest.yml' file in test directory {}".format(self.testdir))
            
        except PrepareFailed:
            errormsg("failed in setting up for building test {}".format(self.testdir))
            
        except BuildFailed:
            errormsg("failed in building test {}".format(self.testdir))
            
        except ExecuteFailed:
            errormsg("failed in excuting test {}".format(self.testdir))
            
        except CheckFailed:
            errormsg("failed in checking result of test {}".format(self.testdir))


    def readTestDescription(self):

        # read yaml file
        from spackle import loadYamlFile
        with open(os.path.join(self.testdir, "hpctest.yml"), 'r') as f:
            desc = loadYamlFile(f)
            
        # validate and apply defaults
        # TODO
            
        return desc
        

    def prepareWorkDir(self, testDesc):

        # prepare test's work workdir and build & run sworkdirs
        workdir  = self.workspace.addWorkDir(os.path.basename(self.testdir), self.config)
        srcdir   = self.testdir
        builddir = os.path.join(workdir, "build"); os.makedirs(builddir)
        rundir   = os.path.join(workdir, "run");   os.makedirs(rundir)
        
        # ...
        
        return (srcdir, builddir, rundir)


    def buildTest(self, testDesc, srcdir, builddir):

        return          # TEMPORARY


    def executeBuiltTest(self, testDesc, builddir, rundir):

       return          # TEMPORARY


    def checkTestResults(self, testDesc, rundir):

        return          # TEMPORARY

        
        
