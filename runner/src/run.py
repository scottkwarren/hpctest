################################################################################
#                                                                              #
#  run.py                                                                      #
#  run a single test case in a new job directory in given workspace            #
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




class Run():
    
    def __init__(self, testdir, config, hpctoolkit, hpctoolkitparams, workspace):
        
        from os.path import basename
        from resultdir import ResultDir
        
        self.testdir   = testdir                        # path to test case's directory
        self.config    = config                         # Spack spec for desired build configuration
        self.workspace = workspace                      # storage for collection of test job dirs
        self.name      = basename(self.testdir)

        # hpctoolkit params
        self.hpctoolkitBinPath = hpctoolkit
        paramList = hpctoolkitparams.split(";")
        self.hpcrunParams    = paramList[0]
        self.hpcstructParams = paramList[1] if len(paramList) >= 2 else ""
        self.hpcprofParams   = paramList[2] if len(paramList) >= 3 else ""
        self.testIncs = "./+"

        # job directory
        configdesc  = self.config    ## TODO: compute description including all dim specs
        self.jobdir = self.workspace.addJobDir(self.name, configdesc)
        
         # storage for hpctest inputs and outputs
        self.output = ResultDir(self.jobdir, "OUT")
        self._writeInputs()
    

    def run(self):
        
        import time
        from common import infomsg, sepmsg
        from common import BadTestDescription, PrepareFailed, BuildFailed, ExecuteFailed, CheckFailed
        
        startTime = time.time()
        sepmsg(True)
        infomsg("running test {} with config {}".format(self.testdir, self.config))
        sepmsg(True)
        
        try:
            
            self._readYaml()
            self._prepareJobDirs()
            self._buildTest()
            self._runBuiltTest()
            self._checkTestResults()
            self.output.addSummaryStatus("OK", None)
            
        except BadTestDescription as e:
            msg = "missing or invalid '{}' file: {}".format("hpctest.yaml", e.message)
        except PrepareFailed as e:
            msg = "failed to set up for building test"
        except BuildFailed as e:
            msg = "failed to build test"
        except ExecuteFailed as e:
            msg = "failed to run test"
        except CheckFailed as e:
            msg = "failed to check test results"
        except Exception as e:
            msg = "unexpected error {} ({})".format(type(e).__name__, e.message)
        else:
            msg = None
        if msg: infomsg(msg)
        
        # finish writing results
        elapsedTime = time.time() - startTime
        self._addMissingOutputs()
        self.output.add("summary", "elapsed time", elapsedTime, format="{:0.2f}")
        self.output.write()



    def _readYaml(self):

        from os.path import join, basename
        import spack
        from common import readYamlforTest, BadTestDescription
        
        self.yaml, msg = readYamlforTest(self.testdir)
        if msg:
            self.output.addSummaryStatus("TEST YAML FAILED", msg)
            raise BadTestDescription(msg)

        # extract important values for easy reference
        self.name = self.yaml["info"]["name"]                               # name of test case
        self.version = self.yaml["info"]["version"]                         # TODO: let 'info.version' be missing, and use package default in such cases
        self.builtin = (self.yaml["config"] == "spack-builtin")

        # get a spec for this test in specified configuration
        namespace = "builtin" if self.builtin else "tests"
        specString = "{}@{}{}".format(namespace + "." + self.name, self.version, self.config)
        try:
            self.spec = spack.cmd.parse_specs(specString)[0]                # TODO: deal better with possibility that returned list length != 1
            self.output.add("input", "spack spec", str(self.spec))
            if "+mpi" in self.spec:
                specString += " +mpi"
                self.spec = spack.cmd.parse_specs(specString)[0]            # TODO: deal better with possibility that returned list length != 1
            if "+openmp" in self.spec:
                specString += " +openmp"
                self.spec = spack.cmd.parse_specs(specString)[0]            # TODO: deal better with possibility that returned list length != 1
            self.spec.concretize()                                          # TODO: check that this succeeds
        except Exception as e:
            self.output.addSummaryStatus("TEST CONFIG INVALID", e.message)
            raise BadTestDescription(e.message)


    def _prepareJobDirs(self):

        from os import makedirs, symlink
        from os.path import basename, join
        from shutil import copytree
        from common import PrepareFailed

        try:
            
            # src directory -- immutable so just use teste's dir
            self.srcdir = self.testdir
            
            # build directory - make new or copy test's dir if not separable-build test
            # TODO: ensure relevant keys are in self.yaml, or handle missing keys here
            self.builddir = join(self.jobdir, "build");
            if "build" in self.yaml["build"]["separate"]:
                makedirs(self.builddir)
            else:
                copytree(self.srcdir, self.builddir)
                symlink( self.builddir, join(self.jobdir, basename(self.srcdir)) )
                
            # run directory - make new or use build dir if not separable-run test
            # TODO: ensure relevant keys are in self.yaml, or handle missing keys here
            if "run" in self.yaml["build"]["separate"]:
                self.rundir = join(self.jobdir, "run");
                makedirs(self.rundir)
            else:
                self.rundir = self.builddir
                
        except Exception as e:
            self.output.addSummaryStatus("TEST INIT FAILED", e.message)
            raise PrepareFailed(e.message)
        

    def _buildTest(self):

        import shutil
        import spack
        from spack.build_environment import ChildError
        from spack.stage import DIYStage
        from spack.package import InstallError
        from llnl.util.tty.log import log_output

        from common import options, infomsg, errormsg, fatalmsg, BuildFailed, ElapsedTimer

        # build the package if necessary
        self.package = spack.repo.get(self.spec)
        if self.package.installed:
            if "verbose" in options: infomsg("skipping build, test already installed")
            status, msg = "OK", "already built"
            buildTime = 0.0
        else:
            if not self.builtin:
                self.package.stage = DIYStage(self.builddir)  # TODO: cf separable vs inseparable builds
            spack.do_checksum = False   # see spack.cmd.diy lines 91-92
            
            outputPath = self.output.makePath("{}-output.txt", "build")
            with log_output(outputPath, echo="verbose" in options):
                with ElapsedTimer() as t:
                    
                    try:
                        self.package.do_install(
                            keep_prefix=False,
                            install_deps=True,
                            verbose="verbose" in options,
                            keep_stage=True,        # don't remove source dir for DIY.
                            explicit=True,
                            dirty=True,             # TODO: cf separable vs inseparable builds
                            force=False)            # don't install if already installed -- TODO: deal with possibility that src may have changed
                        status, msg = "OK", None
                    except Exception as e:
                        status, msg =  "FAILED", str(e)
                        
                buildTime = t.secs

        # save results
        self.prefix = self.package.prefix       # prefix path is valid even if package failed to install
        self.output.add("build", "prefix",     str(self.prefix))
        self.output.add("build", "cpu time",   buildTime, format="{:0.2f}")
        self.output.add("build", "status",     status)
        self.output.add("build", "status msg", msg)

        # finish up
        if status == "OK":
            infomsg("... build time = {:<0.2f} seconds".format(buildTime))
        else:
            if status == "FATAL":
                fatalmsg(msg)
            else:
                errormsg("build failed, " + msg)
                if "verbose" in options:
                    if not os.path.exists(e.pkg.build_log_path):
                        infomsg("...build produced no log.")
                    else:
                        infomsg("...build log:")
                        with open(e.pkg.build_log_path) as log:
                            shutil.copyfileobj(log, sys.stdout)
            self.output.addSummaryStatus("BUILD FAILED", msg)
            raise BuildFailed(msg)


    def _runBuiltTest(self):

        from os import mkdir
        from os.path import join, isdir
        from string import split
        from common import options, infomsg, verbosemsg, sepmsg, ExecuteFailed

        # set up for test case execution
        cmd = self.yaml["run"]["cmd"]
        self.exeName = cmd.split()[0]
        
        # execute test case with and without profiling (to measure overhead)
        normalTime,   normalFailMsg   = self._execute(cmd, ["run"], "normal")
        profiledTime, profiledFailMsg = self._execute(cmd, ["run"], "profiled", profile=True)
        self._checkHpcrunExecution(normalTime, normalFailMsg, profiledTime, profiledFailMsg)
        
        if "verbose" in options: sepmsg()
        
        # run hpcstruct on test executable
        structPath = self.output.makePath("{}.hpcstruct".format(self.exeName))
        cmd = "{}/hpcstruct -o {} {} -I {} {}" \
            .format(self.hpctoolkitBinPath, structPath, self.hpcstructParams, self.testIncs, join(self.prefix.bin, split(self.yaml["run"]["cmd"])[0]))
        structTime, structFailMsg = self._execute(cmd, [], "hpcstruct", mpi=False, openmp=False)
        self._checkHpcstructExecution(structTime, structFailMsg, structPath)
    
        # run hpcprof on test measurements
        if profiledFailMsg or structFailMsg:
            infomsg("... hpcprof not run due to previous failure")
        else:
            profPath = self.output.makePath("hpctoolkit-{}-database".format(self.exeName))
            cmd = "{}/hpcprof -o {} -S {} {} -I {} {}" \
                .format(self.hpctoolkitBinPath, profPath, structPath, self.hpcprofParams, self.testIncs, self.measurementsPath)
            profTime, profFailMsg = self._execute(cmd, [], "hpcprof", mpi=False, openmp=False)
            self._checkHpcprofExecution(profTime, profFailMsg, profPath)
    
        # let caller know if test case failed
        if   normalFailMsg:     failure, msg  = "NORMAL RUN FAILED", normalFailMsg
        elif profiledFailMsg:   failure, msg  = "HPCRUN FAILED",     profiledFailMsg
        elif structFailMsg:     failure, msg  = "HPCSTRUCT FAILED",  structFailMsg
        elif profFailMsg:       failure, msg  = "HPCPROF FAILED",    profFailMsg
        else:                   failure, msg  = None,                None
        
        if failure:
            self.output.addSummaryStatus(failure, msg)
            raise ExecuteFailed
            
    
    def _execute(self, cmd, keylist, label, profile=None, mpi=None, openmp=None, batch=None):

        import os
        from os.path import join
        import sys
        from spack.util.executable import ProcessError
        from spackle import execute
        from common import options, infomsg, verbosemsg, debugmsg, errormsg, fatalmsg, sepmsg, ExecuteFailed
        from configuration import currentConfig
        
        wantProfile = profile if profile else False
        wantMPI     = mpi     if mpi    is not None else '+mpi' in self.spec
        wantOpenMP  = openmp  if openmp is not None else '+openmp' in self.spec
        wantBatch   = batch   if batch  is not None else False     # TODO: figure out from options & package info

        # compute command to be executed
        # ... start with test's run command
        env = os.environ.copy()         # needed b/c execute's subprocess.Popen discards existing environment if 'env' arg given
        env["PATH"] = self.package.prefix + "/bin" + ":" + env["PATH"]
        runPath  = self.rundir if "dir" not in self.yaml["run"] else join(self.rundir, self.yaml["run"]["dir"])
        outPath  = self.output.makePath("{}-output.txt", label)
        timePath = self.output.makePath("{}-time.txt", label)

        # ... add profiling code if wanted
        if profile:
            self.measurementsPath = self.output.makePath("hpctoolkit-{}-measurements".format(self.exeName))
            cmd = "{}/hpcrun -o {} -t {} {}".format(self.hpctoolkitBinPath, self.measurementsPath, self.hpcrunParams, cmd)

        # ... add OpenMP parameters if wanted
        if wantOpenMP:
            if "threads" in self.yaml["run"]:
                openMPNumThreads = str( self.yaml["run"]["threads"] )
                env["OMP_NUM_THREADS"] = openMPNumThreads
        
        # ... add MPI launching code if wanted
        if wantMPI:
            mpiBinPath  = join(self.spec["mpi"].prefix, "bin")
            mpiNumRanks = str( self.yaml["run"]["ranks"] )
            cmd = "{}/mpiexec -np {} {}".format(mpiBinPath, mpiNumRanks, cmd)
        
        # ... add batch scheduling code if wanted
        if wantBatch:
            notimplemented("batch scheduling")   # TODO: implement this
        
        # ... always add timing code
        cmd = "/usr/bin/time -f '%e\\\\\\\\t%S\\\\\\\\t%U' -o {} {}".format(timePath, cmd)   # backslashes are 
        
        # ... always add resource limiting code
        limitstring = self._makeLimitString()
        cmd = " /bin/bash -c 'ulimit {}; {}' ".format(limitstring, cmd)
        
        self.output.add(label, "command", cmd, subroot=keylist)

        # execute the command
        verbosemsg("Executing {} test:\n{}".format(label, cmd))
        try:
            
            with open(outPath, "w") as outf:
                execute(cmd, cwd=runPath, env=env, output=outf, error=outf)
                
        except Exception as e:
            failed, msg = True, "{} ({})".format(type(e).__name__, e.message.rstrip(":"))   # 'rstrip' b/c ProcessError.message ends in ':' fsr
            infomsg("{} execution failed: {}".format(label, msg))
        else:
            failed, msg = False, None
                    
        # print test's output and cpu time
        if "verbose" in options:
            with open(outPath, "r") as f: print f.read()
        cputime = self._readTotalCpuTime(timePath)
        if cputime:
            infomsg("... {} cpu time = {:<0.2f} seconds".format(label, cputime))
        
        # save results
        self.output.add(label, "cpu time", cputime, subroot=keylist, format="{:0.2f}")
        self.output.add(label, "status", "FAILED" if failed else "OK", subroot=keylist)
        self.output.add(label, "status msg", msg, subroot=keylist)
        
        return cputime, msg
    

    def _makeLimitString(self, limitDict=None):
        
        import configuration
        
        unitsDict = {"k": 2**10, "K": 2**10, "m": 2**20, "M": 2**20, "g": 2**30, "G": 2**30}
        
        if not limitDict: limitDict = configuration.get("run.ulimit", {})
        
        s = ""
        for key in limitDict:
            
            value = str(limitDict[key])
            
            if value != "unlimited":
                
                lastChar = value[-1]
                if lastChar in unitsDict:
                    multiplier = unitsDict[lastChar]
                    value = value[:-1]
                else:
                    multiplier = 1
                
                if key == "t":  # cpu time must be apportioned to child processes
                    try:    ranks = self.yaml["run"]["ranks"]
                    except: ranks = 1
                    divisor = ranks
                else:
                    divisor = 1
                    
                value = str( int(value) * multiplier / divisor )

            s += "-{} {} ".format(key, value)
            
        return s

    
    def _readTotalCpuTime(self, timePath):
            
        import csv
        from os.path import join
        
        try:
            
            with open(timePath, "r") as f:
                line = f.read()
                times = csv.reader([line], delimiter="\t").next()
                cpuTime = float(times[1]) + float(times[2])
                
        except Exception as e:
            cpuTime = None
        
        return cpuTime
            

    def _checkTestResults(self):

        pass        # TODO
#       self.output.addSummaryStatus("CHECK FAILED", xxx)
    

    def _writeInputs(self):

        from collections import OrderedDict
        import datetime
        from os.path import join, relpath
        from common import homepath

        now = datetime.datetime.now()
        self.output.add("input", "date", now.strftime("%Y-%m-%d %H:%M"))
        self.output.add("input", "test", relpath(self.testdir, join(homepath, "tests")))
        self.output.add("input", "config spec", str(self.config))
        self.output.add("input", "hpctoolkit", str(self.hpctoolkitBinPath))
        self.output.add("input", "hpctoolkit params", OrderedDict({"hpcrun":self.hpcrunParams, "hpcstruct":self.hpcstructParams, "hpcprof":self.hpcprofParams}))
        self.output.add("input", "workspace", self.workspace.path)
            


    def _addMissingOutputs(self):
        
        if "build" not in self.output:
            self.output.add("build", "NA")
        if "run"   not in self.output:
            self.output.add("run", "NA")
        if "hpcstruct" not in self.output:
            self.output.add("hpcstruct", "NA")
        if "hpcprof" not in self.output:
            self.output.add("hpcprof", "NA")


    def _checkHpcrunExecution(self, normalTime, normalFailMsg, profiledTime, profiledFailMsg):
        
        from common import infomsg

        # compute profiling overhead
        if normalFailMsg or profiledFailMsg:
            infomsg("... hpcrun overhead not computed due to execution failure")
            self.output.add("run", "profiled", "hpcrun overhead %", "NA")
        else:
            overheadPercent = 100.0 * (profiledTime/normalTime - 1.0)
            infomsg("... hpcrun overhead = {:<0.2f} %".format(overheadPercent))
            self.output.add("run", "profiled", "hpcrun overhead %", overheadPercent, format="{:0.2f}")

        # summarize hpcrun log
        if profiledFailMsg:
            infomsg("... hpcrun log not summarized due to execution failure")
            self.output.add("run", "profiled", "hpcrun summary",  "NA")
        else:
            summaryDict = self._summarizeHpcrunLog()
            self.output.add("run", "profiled", "hpcrun summary", summaryDict)
        
        # no checks yet, so always record success
        self.output.add("hpcrun", "output checks", "OK")
        self.output.add("hpcrun", "output msg",    None)


    def _summarizeHpcrunLog(self):
        
        from os import listdir
        from os.path import join, isfile, basename, splitext
        import re, string
        from common import debugmsg, errormsg
        from spackle import writeYamlFile

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
        
        for item in listdir(self.measurementsPath):
            itemPath = join(self.measurementsPath, item)
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
        
        return summedResultDict


    def _checkHpcstructExecution(self, structTime, structFailMsg, structPath):
        
        if structFailMsg:
            msg = structFailMsg
        else:
            msg = self._checkTextFile("structure file", structPath, 66, '<?xml version="1.0"?>\n', "</HPCToolkitStructure>\n")
            
        self.output.add("hpcstruct", "output checks", "FAILED" if msg else "OK")
        self.output.add("hpcstruct", "output msg",    msg)


    def _checkHpcprofExecution(self, profTime, profFailMsg, profPath):
        
        from common import infomsg

        if profFailMsg:
            msg = profFailMsg
        else:
            msg = self._checkTextFile("performance db", profPath, 66, '<?xml version="1.0"?>\n', "</HPCToolkitStructure>\n")
            
        self.output.add("hpcprof", "output checks", "FAILED" if msg else "OK")
        self.output.add("hpcprof", "output msg",    msg)


    def _checkTextFile(self, fileblurb, path, minLen, goodFirstLines, goodLastLines):

        from os.path import isfile

        if isfile(path):
            
            with open(path, "r") as f:
                
                lines = f.readlines()
                if type(goodFirstLines) is not list: goodFirstLines = [ goodFirstLines ]
                if type(goodLastLines)  is not list: goodLastLines  = [ goodLastLines  ]
                
                if len(lines) < 66:                                   msg = "{} is too short".format(fileblurb)
                elif lines[-len(goodFirstLines):] != goodFirstLines:  msg = "{}'s first line is invalid".format(fileblurb)
                elif lines[-len(goodLastLines): ] != goodLastLines:   msg = "{}'s first line is invalid".format(fileblurb)
                else:                                                 msg = None
                
        else:
            msg = "no {} was produced".format(fileblurb)



                                                                                                                                    