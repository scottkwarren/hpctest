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
        self.runOutpath    = self.output.makePath("hpctoolkit-{}-measurements".format(self.name))
        self.structOutpath = self.output.makePath("{}.hpcstruct".format(self.name))
        self.profOutpath   = self.output.makePath("hpctoolkit-{}-database".format(self.name))

     
    def description(self, forName=False):
         
        return "complete hpcrun/hpcstruct/hpcprof profiling run"
     
     
    def perform(self):
         
        from os.path import join
        from run import Run
        from common import options, infomsg, verbosemsg, sepmsg, ExecuteFailed

        # (0) execute test case without profiling
        self.normalTime, self.normalFailMsg = self.runOb.execute(self.cmd, ["run"], "normal", self.wantMPI, self.wantOMP)
         
        # if requested, do full HPCToolkit profiling pipeline
        if self.test.wantProfile():
            
            # hpctoolkit tool parameters
            runParams    = self.profile.hpcrun
            structParams = self.profile.hpcstruct
            profParams   = self.profile.hpcprof
            
            # (1) execute test case with profiling
            runCmd = "{}/hpcrun -o {} -t {} {}" \
                .format(self.hpctoolkitBinPath, self.runOutpath, runParams, self.cmd)
            self.profiledTime, self.profiledFailMsg = self.runOb.execute(runCmd, ["run"], "profiled", self.wantMPI, self.wantOMP)
             
            if "verbose" in options: sepmsg()
             
            # (2) run hpcstruct on test executable
            self.cmdExe = self.cmd.split()[0]
            structCmd = "{}/hpcstruct -o {} {} \"{}\"" \
                .format(self.hpctoolkitBinPath, self.structOutpath, structParams, join(self.prefixBin, self.cmdExe))
            self.structTime, self.structFailMsg = self.runOb.execute(structCmd, ["run", "profiled"], "hpcstruct", False, False)
         
            # (3) run hpcprof on test measurements
            if self.profiledFailMsg or self.structFailMsg:
                infomsg("hpcprof not run due to previous failure")
            else:
                profCmd = "{}/hpcprof -o {} -S {} {} {}" \
                    .format(self.hpctoolkitBinPath, self.profOutpath, self.structOutpath, profParams, self.runOutpath)
                self.profTime, self.profFailMsg = self.runOb.execute(profCmd, ["run", "profiled"], "hpcprof", False, False)
             
            # (4) TODO: open hpcviewer on experiment database (& get it to do something nontrivial, if possible)
            #           -- omplicated b/c hpcviewer is written in Java; need a VM and some kind of UI access (?)
                 
        else:
            verbosemsg("profiling is disabled by hpctest.yaml")
            self.profiledTime, self.profiledFailMsg = 0.0, None
            self.structTime,   self.structFailMsg   = 0.0, None
            self.profTime,     self.profFailMsg     = 0.0, None
     
        # let caller know if test case failed
        if   self.normalFailMsg:    msg = self.normalFailMsg
        elif self.profiledFailMsg:  msg = "HPCRUN FAILED: "    + self.profiledFailMsg
        elif self.structFailMsg:    msg = "HPCSTRUCT FAILED: " + self.structFailMsg
        elif self.profFailMsg:      msg = "HPCPROF FAILED: "   + self.profFailMsg
        else:                       msg = None
         
        if msg:

            raise ExecuteFailed(msg)


    def check(self):
        
        self._checkHpcrunExecution()
        self._checkHpcstructExecution()
        self._checkHpcprofExecution()
    
     
    def _checkHpcrunExecution(self):
         
        from common import infomsg, percentDelta
        from experiment import Experiment
 
        # check outputs from hpcrun
        status, msg = "OK", None
        pass
    
        # compute profiling overhead
        if self.normalFailMsg or self.profiledFailMsg or self.normalTime == 0.0:
            infomsg("hpcrun overhead not computed")
            self.output.add("run", "profiled", "hpcrun", "overhead %", "NA")
            overheadPercent = "NA"
        else:
            overheadPercent = percentDelta(self.profiledTime, self.normalTime)
            infomsg("hpcrun overhead = {:<2s}".format(overheadPercent))
            self.output.add("run", "profiled", "hpcrun", "overhead %", overheadPercent, format="{:0.2f}")
 
        # summarize hpcrun log
        if self.profiledFailMsg:
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
        from common import debugmsg, errormsg, notimplemented
        from util.yaml import writeYamlFile
 
        status, msg = Experiment.checkDirExists("hpcrun log", self.runOutpath)
        if status == "OK":
            
            # prepare to extract results
            pattern = ( "UNWIND ANOMALIES: total: D errant: D, total-frames: D, total-libunwind-fails: D\n"
                        "ACC SUMMARY:\n"
                        "         accelerator trace records: D (processed: D, dropped: D)\n"
                        "         accelerator samples: D (recorded: D, dropped: D)\n"
                        "SAMPLE ANOMALIES: blocks: D (async: D, dlopen: D), errors: D (segv: D, soft: D)\n"
                        "SUMMARY: samples: D (recorded: D, blocked: D, errant: D, trolled: D, yielded: D),\n"
                        "         frames: D (trolled: D)\n"
                        "         intervals: D (suspicious: D)\n"
                      )
            fieldNames = [ "acc-trace-records", "acc-processed", "acc-dropped", "acc-samples", "acc-recorded",
                           "acc-dropped", "acc-blocks", "acc-async", "acc-dlopen", "acc-errors", "acc-segv", "acc-soft"
                           "samples", "recorded", "blocked", "errant", "trolled", "yielded", "frames", "trolled", "intervals", "suspicious" ]
            pattern = string.replace(pattern, r"(", r"\(")
            pattern = string.replace(pattern, r")", r"\)")
            pattern = string.replace(pattern, r" D", r"( \d+)") # note space char at front of each patterns
            rex = re.compile(pattern)
                  
            # summarize the profiling results for each execution
            scrapedResultTupleList = []
            for item in listdir(self.runOutpath):
                itemPath = join(self.runOutpath, item)
                if isfile(itemPath) and (splitext(basename(item))[1])[1:] == "log":     ## was "hpcrun"
                    with open(itemPath, "r") as f:
                        
                        if True:
                            last8lines  = f.readlines()[-8:]
                            summaryLine = "".join(last8lines)
                        else:
                            last3lines  = f.readlines()[-3:]
                            summaryLine = "".join(last3lines)

                        match = rex.match(summaryLine)
                        if match:
                            scrapedResultTuple = map(int, match.groups())   # convert matched strings to ints
                            scrapedResultTupleList.append(scrapedResultTuple)
                        else:
                            errormsg("hpcrun log '{}' has unexpected format:\n{}".format(item, summaryLine))
                             
            summedResultTuple = map(sum, zip(*scrapedResultTupleList))
            summedResultDict  = dict(zip(fieldNames, summedResultTuple))
            sumPath = self.output.makePath("hpcrun-summary.yaml")
            writeYamlFile(sumPath, summedResultDict)
            debugmsg("hpcrun summary = {}".format(summedResultDict))
            
        else:
            debugmsg("hpcrun summary not produced (no hpcrun log)")
            summedResultDict = dict()
             
        return summedResultDict
 
 
    def _checkHpcstructExecution(self):
         
        import xml.etree.ElementTree as ET
        from experiment import Experiment

        if self.structFailMsg:
            status, msg = "NA", self.structFailMsg
        else:
            # check outputs from hpcstruct...
            status, msg = "OK", None
    
            # structure file exists
            len   = 20  # lines
            first = ['<?xml version="1.0"?>\n',
                     '<!DOCTYPE HPCToolkitStructure [\n']
            last  = ['</LM>\n',
                     '</HPCToolkitStructure>\n']
            status, msg = Experiment.checkTextFile("structure file", self.structOutpath, len, first, last)
        
        # parse the (xml) structure file as a coarse validation
        try:
            tree = ET.parse(self.structOutpath)
        except:
            status, msg = "FAILED", "structure file is invalid xml"
            
        # record results
        self.output.add("run", "profiled", "hpcstruct", "output check status", status)
        self.output.add("run", "profiled", "hpcstruct", "output check msg",    msg)
 
 
    def _checkHpcprofExecution(self):
        
        from os.path import join
        from run import Run
        from common import infomsg
        from experiment import Experiment

        if self.profFailMsg:
            status, msg = "FAILED", profFailMsg
        else:
            # check outputs from hpcprof...
            status, msg = "OK", None
    
            # perf db exists and is reasonable
            status, msg = Experiment.checkDirExists("performance db", self.profOutpath)
            if not msg:
                path  = join(self.profOutpath, "experiment.xml")
                len   = 10
                first = ['<?xml version="1.0"?>\n',
                         '<!DOCTYPE HPCToolkitExperiment [\n']
                last  = ['</SecCallPathProfile>\n',
                         '</HPCToolkitExperiment>\n']
                status, msg = Experiment.checkTextFile("experiment file", path, len, first, last)
            
        # record results
        self.output.add("run", "profiled", "hpcprof", "output check status", status)
        self.output.add("run", "profiled", "hpcprof", "output check msg",    msg)




