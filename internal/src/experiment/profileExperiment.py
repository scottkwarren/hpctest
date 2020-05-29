################################################################################
#                                                                              #
#  profileExperiment.py                                                        #
#  run a test case through full HPCTkit profiling workflow:                    #
#    hpcrun -> hpcstruct -> hpcprof [-> hpcviewer]    (viewer not implemented) #
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


from experiment import Experiment


class ProfileExperiment(Experiment):
    

    def __init__(self, test, run, output, build, hpctoolkit, profile):

        from os.path import join

        super(ProfileExperiment, self).__init__(test, run, output)

        # dimension parameters
        self.build = build
        self.hpctoolkitBinPath = join(hpctoolkit, "bin")
        self.profile = profile
         
        # other details
        self.testIncs          = "./+"
    
     
    def description(self, forName=False):
         
        return "some experiment run"
     
     
    def run(self):
         
        self._runProfilePipeline()
        self._checkResults()
 
 
    def _runProfilePipeline(self):
 
        from os.path import join
        from run import Run
        from common import options, infomsg, verbosemsg, sepmsg, ExecuteFailed
 
        # (1) execute test case without profiling
        normalTime, normalFailMsg = self.runOb.execute(self.cmd, ["run"], "normal", self.wantMPI, self.wantOMP)
         
        # if requested, do complete HPCTkit profiling pipeline
        if self.test.wantProfile():
            
            # hpctoolkit tool parameters
            runParams    = self.profile.hpcrun
            structParams = self.profile.hpcstruct
            profParams   = self.profile.hpcprof
            
            # (2) execute test case with profiling
            self.runOutpath = self.output.makePath("hpctoolkit-{}-measurements".format(self.exeName))
 
            runCmd = "{}/hpcrun -o {} -t {} {}" \
                .format(self.hpctoolkitBinPath, self.runOutpath, runParams, self.cmd)
            profiledTime, profiledFailMsg = self.runOb.execute(runCmd, ["run"], "profiled", self.wantMPI, self.wantOMP)
            self._checkHpcrunExecution(normalTime, normalFailMsg, profiledTime, profiledFailMsg)
             
            if "verbose" in options: sepmsg()
             
            # (3) run hpcstruct on test executable
            structOutpath = self.output.makePath("{}.hpcstruct".format(self.exeName))
            structCmd = "{}/hpcstruct -o {} {} -I {} {}" \
                .format(self.hpctoolkitBinPath, structOutpath, structParams, self.testIncs, join(self.prefixBin, self.exeName))
            structTime, structFailMsg = self.runOb.execute(structCmd, ["run", "profiled"], "hpcstruct", False, False)
            self._checkHpcstructExecution(structTime, structFailMsg, structOutpath)
         
            # (4) run hpcprof on test measurements
            if profiledFailMsg or structFailMsg:
                infomsg("hpcprof not run due to previous failure")
            else:
                profOutpath = self.output.makePath("hpctoolkit-{}-database".format(self.exeName))
                profCmd = "{}/hpcprof -o {} -S {} {} -I {} {}" \
                    .format(self.hpctoolkitBinPath, profOutpath, structOutpath, profParams, self.testIncs, self.runOutpath)
                profTime, profFailMsg = self.runOb.execute(profCmd, ["run", "profiled"], "hpcprof", False, False)
                self._checkHpcprofExecution(profTime, profFailMsg, profOutpath)
             
            # (5) TODO: open hpcviewer on experiment database (& get it to do something nontrivial, if possible)
            #           -- omplicated b/c hpcviewer is written in Java; need a VM and some kind of UI access (?)
                 
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
     
     
    def _checkResults(self):
 
        pass        # TODO
#       self.output.addSummaryStatus("CHECK FAILED", xxx)
 
     
    def _checkHpcrunExecution(self, normalTime, normalFailMsg, profiledTime, profiledFailMsg):
         
        from common import infomsg
        from experiment import Experiment
 
        # check outputs from hpcrun
        status, msg = "OK", None
        pass
    
        # compute profiling overhead
        if normalFailMsg or profiledFailMsg or normalTime == 0.0:
            infomsg("hpcrun overhead not computed")
            self.output.add("run", "profiled", "hpcrun", "overhead %", "NA")
            overheadPercent = "NA"
        else:
            overheadPercent = 100.0 * (profiledTime/normalTime - 1.0)
            infomsg("hpcrun overhead = {:<0.2f} %".format(overheadPercent))
            self.output.add("run", "profiled", "hpcrun", "overhead %", overheadPercent, format="{:0.2f}")
 
        # summarize hpcrun log
        if profiledFailMsg:
            infomsg("hpcrun log not summarized")
            self.output.add("run", "profiled", "hpcrun", "summary",  "NA")
        else:
            summaryDict = self._summarizeHpcrunLog()
            self.output.add("run", "profiled", "hpcrun", "summary", summaryDict)
         
        # record results
        self.output.add("run", "profiled", "hpcrun", "output check status", status)
        self.output.add("run", "profiled", "hpcrun", "output check msg",    msg)
 
 
    def _summarizeHpcrunLog(self):
         
        from os import listdir
        from os.path import join, isdir, isfile, basename, splitext
        import re, string
        from common import debugmsg, errormsg
        from spackle import writeYamlFile
 
        if isdir(self.runOutpath):
             
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
             
            for item in listdir(self.runOutpath):
                itemPath = join(self.runOutpath, item)
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
         
        from experiment import Experiment

        if structFailMsg:
            status, msg = "NA", structFailMsg
        else:
            # check outputs from hpcstruct...
            status, msg = "OK", None
    
            # structure file exists
            len   = 20  # lines
            first = ['<?xml version="1.0"?>\n',
                     '<!DOCTYPE HPCToolkitStructure [\n']
            last  = ['</LM>\n',
                     '</HPCToolkitStructure>\n']
            status, msg = Experiment.checkTextFile("structure file", structOutpath, len, first, last)
        
        # record results
        self.output.add("run", "profiled", "hpcstruct", "output check status", status)
        self.output.add("run", "profiled", "hpcstruct", "output check msg",    msg)
 
 
    def _checkHpcprofExecution(self, profTime, profFailMsg, profOutpath):
        
        from os.path import join
        from run import Run
        from common import infomsg
        from experiment import Experiment

        if profFailMsg:
            status, msg = "FAILED", profFailMsg
        else:
            # check outputs from hpcprof...
            status, msg = "OK", None
    
            # perf db exists and is reasonable
            status, msg = Experiment.checkDirExists("performance db", profOutpath)
            if not msg:
                path  = join(profOutpath, "experiment.xml")
                len   = 10
                first = ['<?xml version="1.0"?>\n',
                         '<!DOCTYPE HPCToolkitExperiment [\n']
                last  = ['</SecCallPathProfile>\n',
                         '</HPCToolkitExperiment>\n']
                status, msg = Experiment.checkTextFile("experiment file", path, len, first, last)
            
        # record results
        self.output.add("run", "profiled", "hpcprof", "output check status", status)
        self.output.add("run", "profiled", "hpcprof", "output check msg",    msg)




