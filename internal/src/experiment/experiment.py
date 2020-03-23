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
    

    def __init__(self, run,
                cmd, packagePrefix, rundir, runSubdir,    # pre-built test case to use
                numRanks, numThreads, wantMPI, wantOMP,   # runtime details for test case
                output):                                  # recordkeeping details
        
        from os.path import join

        # save parameters
        self.runOb      = run
        self.cmd        = cmd
        self.prefixBin  = join(packagePrefix, "bin")
        self.rundir     = rundir
        self.runSubdir  = runSubdir
        self.numRanks   = numRanks
        self.numThreads = numThreads
        self.wantMPI    = wantMPI
        self.wantOMP    = wantOMP
 
        self.absCmd     = join(self.prefixBin, cmd)
        self.exeName    = cmd.split()[0]
       
#         self.config            = config         # Spack spec for desired build configuration
#         self.hpctoolkitBinPath = join(hpctoolkit, "bin")
#         self.hpctoolkitParams  = profile.strip(" ;:").replace(";", ":")
#         paramList              = self.hpctoolkitParams.split(":")
#         self.hpcrunParams      = paramList[0]
#         self.hpcstructParams   = paramList[1] if len(paramList) >= 2 else ""
#         self.hpcprofParams     = paramList[2] if len(paramList) >= 3 else ""
#         self.wantProfiling     = wantProfiling
        
        self.output            = output
        
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
        normalTime, normalFailMsg = self.runOb.execute(self.absCmd, ["run"], "normal", self.wantMPI, self.wantOMP)
        
        # if requested, do complete HPCTkit profiling pipeline
        if self.wantProfiling:
            
            # (2) execute test case with profiling
            runOutpath = self.output.makePath("hpctoolkit-{}-measurements".format(self.exeName))

            runCmd = "{}/hpcrun -o {} -t {} {}" \
                .format(self.hpctoolkitBinPath, runOutpath, self.hpcrunParams, self.absCmd)
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

    
    def _checkHpcrunExecution(self, runOutpath, normalTime, normalFailMsg, profiledTime, profiledFailMsg):
        
        from common import infomsg

        # compute profiling overhead
        if normalFailMsg or profiledFailMsg or normalTime == 0.0:
            infomsg("hpcrun overhead not computed")
            self.output.add("run", "profiled", "hpcrun overhead %", "NA")
            overheadPercent = "NA"
        else:
            overheadPercent = 100.0 * (profiledTime/normalTime - 1.0)
            infomsg("hpcrun overhead = {:<0.2f} %".format(overheadPercent))
            self.output.add("run", "profiled", "hpcrun overhead %", overheadPercent, format="{:0.2f}")

        # summarize hpcrun log
        if profiledFailMsg:
            infomsg("hpcrun log not summarized")
            self.output.add("run", "profiled", "hpcrun summary",  "NA")
        else:
            summaryDict = self._summarizeHpcrunLog(runOutpath)
            self.output.add("run", "profiled", "hpcrun summary", summaryDict)
        
        # no checks yet, so always record success
        self.output.add("run", "hpcrun", "output checks", "OK")
        self.output.add("run", "hpcrun", "output msg",    None)


    def _summarizeHpcrunLog(self, runOutpath):
        
        from os import listdir
        from os.path import join, isdir, isfile, basename, splitext
        import re, string
        from common import debugmsg, errormsg
        from spackle import writeYamlFile

        if isdir(runOutpath):
            
            pattern = ( "SUMMARY: samples: D (recorded: D, blocked: D, errant: D, trolled: D, yielded: D),\n"
                        "         frames: D (trolled: D)\n"
                        "         intervals: D (suspicious: D)\n"
                      )
            fieldNames = [ "samples", "recorded", "blocked", "errant", "trolled", "yielded", "frames", "trolled", "intervals", "suspicious" ]
            pattern = string.replace(pattern, r"(", r"\(")
            pattern = string.replace(pattern, r")", r"\)")
            pattern = string.replace(pattern, r"D", r"(\d+)")
            rex = re.compile(pattern)
    
            scrapedResultTupleList = []
            
            for item in listdir(runOutpath):
                itemPath = join(runOutpath, item)
                if isfile(itemPath) and (splitext(basename(item))[1])[1:] == "log":
                    with open(itemPath, "r") as f:
                        
                        last3lines  = f.readlines()[-3:]
                        summaryLine = "".join(last3lines)
                        match = rex.match(summaryLine)
                        if match:
                            scrapedResultTuple = map(int, match.groups())   # convert matched strings to ints
                            scrapedResultTupleList.append(scrapedResultTuple)
                        else:
                            errormsg("hpcrun log '{}' has summary with unexpected format:\n{}".format(item, summaryLine))
                            
            summedResultTuple = map(sum, zip(*scrapedResultTupleList))
            summedResultDict  = dict(zip(fieldNames, summedResultTuple))
            sumPath = self.output.makePath("hpcrun-summary.yaml")
            writeYamlFile(sumPath, summedResultDict)
            debugmsg("hpcrun summary = {}".format(summedResultDict))
        
        else:
            summedResultDict = "NA"
            
        return summedResultDict


    def _checkHpcstructExecution(self, structTime, structFailMsg, structOutpath):
        
        from run import Run

        if structFailMsg:
            msg = structFailMsg
        else:
            msg = self.runOb.checkTextFile("structure file", structOutpath, 66, '<?xml version="1.0"?>\n', "</HPCToolkitStructure>\n")
            
        self.output.add("run", "hpcstruct", "output checks", "FAILED" if msg else "OK")
        self.output.add("run", "hpcstruct", "output msg",    msg)


    def _checkHpcprofExecution(self, profTime, profFailMsg, profOutpath):
        
        from run import Run
        from common import infomsg

        if profFailMsg:
            msg = profFailMsg
        else:
            msg = self.runOb.checkTextFile("performance db", profOutpath, 66, '<?xml version="1.0"?>\n', "</HPCToolkitStructure>\n")
            
        self.output.add("run", "hpcprof", "output checks", "FAILED" if msg else "OK")
        self.output.add("run", "hpcprof", "output msg",    msg)
    


   

