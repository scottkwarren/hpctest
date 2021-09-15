################################################################################
#                                                                              #
#  experiment.py                                                               #
#  abstract superclass for all experiment classes in HPCTest                   #
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




class Experiment(object):
    

    def __init__(self, test, run, output):
        
        from os.path import join

        # creation parameters
        self.test       = test
        self.runOb      = run
        self.prefixBin  = join(run.packagePrefix, "bin")
        self.rundir     = run.rundir
        self.output     = output

        # derived values
        self.cmd        = self.test.cmd()
        self.runSubdir  = self.test.runSubdir()
        self.numRanks   = self.test.numRanks()
        self.numThreads = self.test.numThreads()
        self.wantMPI    = self.numRanks > 0
        self.wantOMP    = self.numThreads > 0
        self.exeName    = self.cmd.split()[0]
        
        # other detailss
        self.testIncs          = "./+"
    
    
    def description(self, forName=False):
        
        from common import subclassResponsibility
        subclassResponsibility("Experiment", "description")
    
    
    def run(self):
        
        self.perform()
        self.check()
    
    
    def perform(self):
        
        from common import subclassResponsibility
        subclassResponsibility("Experiment", "perform")


    def check(self):
        
        from common import subclassResponsibility
        subclassResponsibility("Experiment", "check")
    

    @classmethod
    def checkDirExists(cls, description, path):

        from os.path import isdir

        if isdir(path):
            msg = None
        else:
            msg = "no {} was produced at {}".format(description, path)
        
        status = "FAILED" if msg else "OK"
        return status, msg


    @classmethod
    def checkFileExists(cls, description, path):

        from os.path import isfile

        if isfile(path):
            msg = None
        else:
            msg = "no {} was produced at {}".format(description, path)
        
        status = "FAILED" if msg else "OK"
        return status, msg


    @classmethod
    def checkTextFile(cls, description, path, minLen, goodFirstLines, goodLastLines):

        from os.path import isfile

        msg = None

        if isfile(path):
            
            with open(path, "r") as f:
                
                lines = f.readlines()
                if type(goodFirstLines) is not list: goodFirstLines = [ goodFirstLines ]
                if type(goodLastLines)  is not list: goodLastLines  = [ goodLastLines  ]
                
                n = len(lines)
                plural = "s are" if n > 1 else " is"
                if n < minLen:                                        msg = "{} is too short ({} < {})".format(description, n, minLen)
                elif lines[0:len(goodFirstLines)] != goodFirstLines:  msg = "{}'s first line{} invalid".format(description, plural)
                elif lines[-len(goodLastLines): ] != goodLastLines:   msg = "{}'s first line{} invalid".format(description, plural)
                else:                                                 msg = None
                
        else:
            msg = "no {} was produced at {}".format(description, path)
        
        status = "FAILED" if msg else "OK"
        return status, msg

    


   

