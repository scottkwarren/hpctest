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
    

    def __init__(self,
                 cmd, packagePrefix, mpiPrefix, rundir, runSubdir,  # pre-built test case to use
                 numRanks, numThreads, wantMPI, wantOMP,            # runtime details for test case
                 config, hpctoolkit, profile, wantProfiling,        # test-matrix coordinates
                 output):                                           # recordkeeping details
        
        from os.path import join

        # save parameters
        self.cmd               = cmd
        self.exeName           = cmd.split()[0]
        self.prefixBin         = join(packagePrefix, "bin")
        self.mpiPrefixBin      = join(mpiPrefix, "bin") if mpiPrefix else None
        self.rundir            = rundir
        self.runSubdir         = runSubdir
        self.numRanks          = numRanks
        self.numThreads        = numThreads
        self.wantMPI           = wantMPI
        self.wantOMP           = wantOMP
        
        self.config            = config         # Spack spec for desired build configuration
        self.hpctoolkitBinPath = join(hpctoolkit, "bin")
        self.hpctoolkitParams  = profile.strip(" ;:").replace(";", ":")
        paramList              = self.hpctoolkitParams.split(":")
        self.hpcrunParams      = paramList[0]
        self.hpcstructParams   = paramList[1] if len(paramList) >= 2 else ""
        self.hpcprofParams     = paramList[2] if len(paramList) >= 3 else ""
        self.wantProfiling     = wantProfiling
        
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
        from common import options, infomsg, verbosemsg, sepmsg, ExecuteFailed

        # (1) execute test case without profiling
        normalTime, normalFailMsg = self._execute(self.cmd, ["run"], "normal",  profile=False)
        
        # if requested, do complete HPCTkit profiling pipeline
        if self.wantProfiling:
            
            # (2) execute test case with profiling
            self.hprunOutputPath = self.output.makePath("hpctoolkit-{}-measurements".format(self.exeName))
            profiledTime, profiledFailMsg = self._execute(self.cmd, ["run"], "profiled", profile=True)
            self._checkHpcrunExecution(normalTime, normalFailMsg, profiledTime, profiledFailMsg)
            
            if "verbose" in options: sepmsg()
            
            # (3) run hpcstruct on test executable
            structPath = self.output.makePath("{}.hpcstruct".format(self.exeName))
            structCmd = "{}/hpcstruct -o {} {} -I {} {}" \
                .format(self.hpctoolkitBinPath, structPath, self.hpcstructParams, self.testIncs, join(self.prefixBin, self.exeName))
            structTime, structFailMsg = self._execute(structCmd, ["run", "profiled"], "hpcstruct", profile=False, mpi=False, openmp=False)
            self._checkHpcstructExecution(structTime, structFailMsg, structPath)
        
            # (4) run hpcprof on test measurements
            if profiledFailMsg or structFailMsg:
                infomsg("hpcprof not run due to previous failure")
            else:
                profPath = self.output.makePath("hpctoolkit-{}-database".format(self.exeName))
                profCmd = "{}/hpcprof -o {} -S {} {} -I {} {}" \
                    .format(self.hpctoolkitBinPath, profPath, structPath, self.hpcprofParams, self.testIncs, self.hprunOutputPath)
                profTime, profFailMsg = self._execute(profCmd, ["run", "profiled"], "hpcprof", profile=False, mpi=False, openmp=False)
                self._checkHpcprofExecution(profTime, profFailMsg, profPath)
            
            # TODO: (5) open hpcviewer on experiment database (& get it to do something nontrivial, if possible)
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
    
    
    def _execute(self, cmd, subroot, label,  profile=None, mpi=None, openmp=None):

        import os
        from os.path import join
        import sys
        from subprocess import CalledProcessError
        from common import options, escape, infomsg, verbosemsg, debugmsg, errormsg, fatalmsg, sepmsg
        from common import HPCTestError, ExecuteFailed
        from configuration import currentConfig
        from run import Run
        
        # respect caller's desired for this specific execution
        if profile is None: profile = self.wantProfiling
        if mpi     is None: mpi     = self.wantMPI
        if openmp  is None: openmp  = self.wantOMP
        
        # compute command to be executed
        # ... start with test's run command
        env = os.environ.copy()         # needed b/c execute's subprocess.Popen discards existing environment if 'env' arg given
        env["PATH"] = self.prefixBin + ":" + env["PATH"]
        runPath  = join(self.rundir, self.runSubdir) if self.runSubdir else self.rundir
        outPath  = self.output.makePath("{}-output.txt", label)
        timePath = self.output.makePath("{}-time.txt", label)

        # ... add profiling code if wanted
        if profile:
            cmd = "{}/hpcrun -o {} -t {} {}".format(self.hpctoolkitBinPath, self.hprunOutputPath, self.hpcrunParams, cmd)

        # ... add OpenMP parameters if wanted
        if openmp:
            threads = self.numThreads
            env["OMP_NUM_THREADS"] = str(threads)
        else:
            threads = 1
        
        # ... add MPI launching code if wanted
        if mpi:
            ranks      = self.numRanks
            options    = "-verbose" if "verbose" in options else ""
            cmd        = "{}/mpiexec -np {} {} {}".format(self.mpiPrefixBin, ranks, options, cmd)
        else:
            ranks = 1
        
        # ... always add timing code
        cmd = "/usr/bin/time -f \"%e %S %U\" -o {} {}".format(timePath, cmd)
        
        # ... always add resource limiting code
        limitstring = self._makeLimitString()
        cmd = "/bin/bash -c \"ulimit {}; {}\" ".format(limitstring, escape(cmd))
        
        self.output.add(label, "command", cmd, subroot=subroot)
            
        # execute the command
        verbosemsg("Executing {} test:\n{}".format(label, cmd))
        msg = None  # for cpu-time messaging below
        try:
            
            Run.executor.run(cmd, runPath, env, ranks, threads, outPath, self.description())
                
        except HPCTestError as e:
            failed, msg = True, str(e)
        except Exception as e:
            failed, msg = True, "{} ({})".format(type(e).__name__, e.message.rstrip(":"))   # 'rstrip' b/c CalledProcessError.message ends in ':' fsr
        else:
            failed, msg = False, None
            
        if failed:
            infomsg("{} execution failed: {}".format(label, msg))

        # print test's output and cpu time
        if "verbose" in options:
            with open(outPath, "r") as f:
                print f.read()
            
        if failed:
            cputime, errno, errmsg = None, 0, None
        else:
            cputime, errno, errmsg = self._readTotalCpuTime(timePath)
            if errno == 0:
                infomsg("{} cpu time = {:<0.2f} seconds".format(label, cputime))
            else:
                cputime_msg = "{} cpu time collection failed: ({}) {}".format(label, errno, errmsg)
                infomsg(cputime_msg)
                if not msg:
                    msg = cputime_msg            
        
        # save results
        cpCmd = "cd {}; cp core.* {}  > /dev/null 2>&1".format(runPath, self.output.getDir())
        os.system(escape(cpCmd))
        self.output.add(label, "cpu time", cputime, subroot=subroot, format="{:0.2f}" if cputime else None)
        self.output.add(label, "status", "FAILED" if failed else "OK", subroot=subroot)
        self.output.add(label, "status msg", msg, subroot=subroot)
        
        return cputime, msg
            
    
    def _makeLimitString(self, limitDict=None):
        
        import configuration
        
        unitsDict = {"k": 2**10, "K": 2**10, "m": 2**20, "M": 2**20, "g": 2**30, "G": 2**30}
        
        if not limitDict:
            limitDict = configuration.get("run.ulimit", {})
        
        s = ""
        for key in limitDict:
            
            value = str(limitDict[key])
            
            if value != "unlimited":
                
                # check for units modifier, e.g. '16K'
                lastChar = value[-1]
                if lastChar in unitsDict:
                    multiplier = unitsDict[lastChar]
                    value = value[:-1]
                else:
                    multiplier = 1
                
                # limit on cpu time is a special case
                if key == "t":
                    # time must be divided among child processes
                    divisor = self.numRanks
                else:
                    divisor = 1
                    
                # compute effective limit accordingly
                value = str( int(value) * multiplier / divisor )

            # append a limit option for this resource
            s += "-{} {} ".format(key, value)
            
        return s

    
    def _readTotalCpuTime(self, timePath):
            
        import csv
        
        try:
            
            with open(timePath, "r") as f:
                line = f.read()
                times = csv.reader([line], delimiter=" ").next()
                cpuTime = float(times[1]) + float(times[2])
                
        except IOError as e:
            cpuTime    = None
            errno, msg = e.errno, e.strerror + " " + e.filename
        except Exception as e:
            cpuTime    = None
            errno, msg = e.errno, e.message
        else:
            errno, msg = 0, None
        
        return cpuTime, errno, msg
            

    def _checkTestResults(self):

        pass        # TODO
#       self.output.addSummaryStatus("CHECK FAILED", xxx)

    
    def _checkHpcrunExecution(self, normalTime, normalFailMsg, profiledTime, profiledFailMsg):
        
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
            summaryDict = self._summarizeHpcrunLog()
            self.output.add("run", "profiled", "hpcrun summary", summaryDict)
        
        # no checks yet, so always record success
        self.output.add("run", "hpcrun", "output checks", "OK")
        self.output.add("run", "hpcrun", "output msg",    None)


    def _summarizeHpcrunLog(self):
        
        from os import listdir
        from os.path import join, isdir, isfile, basename, splitext
        import re, string
        from common import debugmsg, errormsg
        from spackle import writeYamlFile

        if isdir(self.hprunOutputPath):
            
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
            
            for item in listdir(self.hprunOutputPath):
                itemPath = join(self.hprunOutputPath, item)
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


    def _checkHpcstructExecution(self, structTime, structFailMsg, structPath):
        
        if structFailMsg:
            msg = structFailMsg
        else:
            msg = self._checkTextFile("structure file", structPath, 66, '<?xml version="1.0"?>\n', "</HPCToolkitStructure>\n")
            
        self.output.add("run", "hpcstruct", "output checks", "FAILED" if msg else "OK")
        self.output.add("run", "hpcstruct", "output msg",    msg)


    def _checkHpcprofExecution(self, profTime, profFailMsg, profPath):
        
        from common import infomsg

        if profFailMsg:
            msg = profFailMsg
        else:
            msg = self._checkTextFile("performance db", profPath, 66, '<?xml version="1.0"?>\n', "</HPCToolkitStructure>\n")
            
        self.output.add("run", "hpcprof", "output checks", "FAILED" if msg else "OK")
        self.output.add("run", "hpcprof", "output msg",    msg)


    def _checkTextFile(self, description, path, minLen, goodFirstLines, goodLastLines):

        from os.path import isfile

        if isfile(path):
            
            with open(path, "r") as f:
                
                lines = f.readlines()
                if type(goodFirstLines) is not list: goodFirstLines = [ goodFirstLines ]
                if type(goodLastLines)  is not list: goodLastLines  = [ goodLastLines  ]
                
                n = len(lines)
                plural = "s are" if n > 1 else " is"
                if n < minLen:                                        msg = "{} is too short ({} < {})".format(description, n, minLen)
                elif lines[-len(goodFirstLines):] != goodFirstLines:  msg = "{}'s first line{} invalid".format(description, plural)
                elif lines[-len(goodLastLines): ] != goodLastLines:   msg = "{}'s first line{} invalid".format(description, plural)
                else:                                                 msg = None
                
        else:
            msg = "no {} was produced".format(description)
    


   

