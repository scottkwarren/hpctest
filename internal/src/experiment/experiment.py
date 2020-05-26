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
    

    def __init__(self, test, run, packagePrefix, rundir, output):
        
        from os.path import join

        # creation parameters
        self.test       = test
        self.runOb      = run
        self.prefixBin  = join(packagePrefix, "bin")
        self.rundir     = rundir
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
        
        return "some experiment run"
    
    
    def run(self):
        
        self._runBuiltTest()
        self._checkTestResults()


    def _runBuiltTest(self):

        from os.path import join
        from run import Run
        from common import options, infomsg, verbosemsg, sepmsg, ExecuteFailed

        # (1) execute test case without profiling
        normalTime, normalFailMsg = self.runOb.execute(self.cmd, ["run"], "normal", self.wantMPI, self.wantOMP)
        
        # if requested, do complete HPCTkit profiling pipeline
        if self.wantProfiling and not normalFailMsg:
            
                # (2) execute test case with profiling
                runOutpath = self.output.makePath("hpctoolkit-{}-measurements".format(self.exeName))
    
                runCmd = "{}/hpcrun -o {} -t {} {}" \
                    .format(self.hpctoolkitBinPath, runOutpath, self.hpcrunParams, self.cmd)
                profiledTime, profiledFailMsg = self.runOb.execute(runCmd, ["run"], "profiled", self.wantMPI, self.wantOMP)
                self._checkHpcrunExecution(runOutpath, normalTime, normalFailMsg, profiledTime, profiledFailMsg)
                
                if "verbose" in options: sepmsg()
                
                # (3) run hpcstruct on test executable
                structOutpath = self.output.makePath("{}.hpcstruct".format(self.exeName))
                structCmd = "{}/hpcstruct -o {} {} -I {} {}" \
                    .format(self.hpctoolkitBinPath, structOutpath, self.hpcstructParams, self.testIncs, join(self.prefixBin, self.exeName))
                structTime, structFailMsg = self.runOb.execute(structCmd, ["run", "profiled"], "hpcstruct", False, False)
                self._checkHpcstructExecution(structTime, structFailMsg, structOutpath)
            
                # (4) run hpcprof on test measurements
                if profiledFailMsg or structFailMsg:
                    infomsg("hpcprof not run due to previous failure")
                else:
                    profOutpath = self.output.makePath("hpctoolkit-{}-database".format(self.exeName))
                    profCmd = "{}/hpcprof -o {} -S {} {} -I {} {}" \
                        .format(self.hpctoolkitBinPath, profOutpath, structOutpath, self.hpcprofParams, self.testIncs, runOutpath)
                    profTime, profFailMsg = self.runOb.execute(profCmd, ["run", "profiled"], "hpcprof", False, False)
                    self._checkHpcprofExecution(profTime, profFailMsg, profOutpath)
                
                # (5) TODO: open hpcviewer on experiment database (& get it to do something nontrivial, if possible)
                #           -- complicated b/c hpcviewer is written in Java; need a VM and some kind of UI access (?)
                
        else:
            if normalFailMsg:
                infomsg("profiling not done due to previous failure")
            else:
                verbosemsg("profiling is disabled by hpctest.yaml")
            profiledTime, profiledFailMsg = 0.0, None
            structTime,   structFailMsg   = 0.0, None
            profTime, profFailMsg         = 0.0, None
    
        # let caller know if test case failed
        if   normalFailMsg:     failure, msg  = "NORMAL RUN FAILED", normalFailMsg
        elif profiledFailMsg:   failure, msg  = "HPCRUN FAILED",     profiledFailMsg
        elif structFailMsg:     failure, msg  = "HPCSTRUCT FAILED",  structFailMsg
        elif profFailMsg:       failure, msg  = "HPCPROF FAILED",    profFailMsg
        else:                   failure, msg  = None,                None
        
        if failure:
            self.output.addSummaryStatus(failure, msg)
            raise ExecuteFailed(msg)
    
    
    def _checkTestResults(self):

        pass        # TODO
#       self.output.addSummaryStatus("CHECK FAILED", xxx)


    @classmethod
    def checkDirExists(cls, description, path):

        from os.path import isdir

        if isdir(path):
            msg = None
        else:
            msg = "no {} was produced".format(description)
        
        status = "FAILED" if msg else "OK"
        return status, msg


    @classmethod
    def checkFileExists(cls, description, path):

        from os.path import isfile

        if isfile(path):
            msg = None
        else:
            msg = "no {} was produced".format(description)
        
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
            msg = "no {} was produced".format(description)
        
        status = "FAILED" if msg else "OK"
        return status, msg

    


   

