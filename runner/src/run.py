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
    
    def __init__(self, testdir, config, workspace):
        
        self.testdir   = testdir                        # path to test case's directory
        self.config    = config                         # Spack spec for desired build configuration
        self.workspace = workspace                      # storage for collection of test job dirs

        # hpctoolkit paths -- TODO: get from setup or environment
        self.hpctoolkitBinPath = "/home/scott/hpctoolkit-current/hpctoolkit/INSTALL/bin"
        self.hpcrunParams      = "-e REALTIME@10000"
        self.hpcstructParams   = ""
        self.hpcprofParams     = ""
        self.testIncs          = "./+"


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
            self.output.add("summary", "status", "OK")
            self.output.add("summary", "status msg", None)
            
        except BadTestDescription as e:
            msg = "missing or invalid '{}' file in test {}".format("hpctest.yaml", self.testdir)
        except PrepareFailed as e:
            msg = "failed while setting up for building test {}".format(self.testdir)
        except BuildFailed as e:
            msg = "failed to build test {}".format(self.testdir)
        except ExecuteFailed as e:
            msg = "failed while running test {}".format(self.testdir)
        except CheckFailed as e:
            msg = "failed while checking test results {}".format(self.testdir)
        except Exception as e:
            msg = "unexpected error in test {} - {} ({})".format(self.testdir, type(e).__name__, e.message)
        else:
            msg = None
        if msg: infomsg(msg)
        
        # finish writing results
        elapsedTime = time.time() - startTime
        self.output.add("summary", "elapsed time", elapsedTime)
        self.output.write()



    def _readYaml(self):

        from os.path import join, basename
        import spack
        from spackle import readYamlFile
        from common import BadTestDescription
        
        # read yaml file
        self.yaml, msg = readYamlFile( join(self.testdir, "hpctest.yaml") )
        if msg:
            self.output.add("summary", "status", "READ TEST INFO FAILED")
            self.output.add("summary", "status msg", msg)
            raise BadTestDescription(error)
    
        # validate and apply defaults
        if not self.yaml.get("info"):
            self.yaml["info"] = {}
        if not self.yaml.get("info").get("name"):
            self.yaml["info"]["name"] = basename(testDir)
        # ... TODO more of this

        # get a spec for this test in specified configuration
        self.name = self.yaml["info"]["name"]                           # name of test case
        version = self.yaml["info"]["version"]
        specString = "{}@{}{}".format("tests." + self.name, version, self.config)
        self.spec = spack.cmd.parse_specs(specString)[0]                # TODO: deal better with possibility that returned list length != 1
        if "+mpi" in self.spec:
            specString += " +mpi"
            self.spec = spack.cmd.parse_specs(specString)[0]            # TODO: deal better with possibility that returned list length != 1
        if "+openmp" in self.spec:
            specString += " +openmp"
            self.spec = spack.cmd.parse_specs(specString)[0]            # TODO: deal better with possibility that returned list length != 1
        self.spec.concretize()     # TODO: check that this succeeds


    def _prepareJobDirs(self):

        from os import makedirs, symlink
        from os.path import basename, join
        from shutil import copytree
        from resultdir import ResultDir

        try:
            
            # job directory
            self.jobdir = self.workspace.addJobDir(self.name, self.config)
            
             # storage for hpctest inputs and outputs
            self.output = ResultDir(self.jobdir, "OUT")
            self._writeInputs()
    
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
            self.output.add("summary", "status", "TEST INIT FAILED")
            self.output.add("summary", "status msg", e.message)
            raise PrepareFailed
        

    def _buildTest(self):

        import shutil
        import spack
        from spack.stage import DIYStage
        from spack.package import InstallError
        from llnl.util.tty.log import log_output

        from common import options, infomsg, errormsg, BuildFailed

        # build the package if necessary
        self.package = spack.repo.get(self.spec)
        if self.package.installed:
            if "verbose" in options: infomsg("Skipping build, test already built")
            status, msg = "OK", "already built"
        else:
            self.package.stage = DIYStage(self.builddir)  # TODO: cf separable vs inseparable builds
            spack.do_checksum = False   # see spack.cmd.diy lines 91-92
            
            outputPath = self.output.makePath("{}-output.txt", "build")
            with log_output(outputPath, echo="verbose" in options):
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

                except InstallError as e:
                    status, msg =  "FAILED", str(e)
                except Exception as e:
                    status, msg = "FATAL", "{} ({})".format(e.message, e.args)

        # save results
        self.prefix = self.package.prefix       # prefix path is valid even if package failed to install
        self.output.add("build", "prefix",     str(self.prefix))
        self.output.add("build", "status",     status)
        self.output.add("build", "status msg", msg)

        # finish up
        if status != "OK":
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
            self.output.add("summary", "status", "BUILD FAILED")
            self.output.add("summary", "status msg", msg)
            raise BuildFailed


    def _runBuiltTest(self):

        from os import mkdir
        from os.path import join, isdir
        from string import split
        from common import options, infomsg, verbosemsg, sepmsg, ExecuteFailed

        # set up for test case execution
        cmd = self.yaml["run"]["cmd"]
        exeName = cmd.split()[0]
        self.measurementsPath = self.output.makePath("hpctoolkit-{}-measurements".format(exeName))
        
        # execute test case with and without profiling (to measure overhead)
        cmd = self.yaml["run"]["cmd"]
        normalTime,   normalFailMsg   = self._execute(cmd, ["run"], "normal")
        profiledTime, profiledFailMsg = self._execute(cmd, ["run"], "profiled", profile=True)
        self._checkHpcrunExecution(normalTime, normalFailMsg, profiledTime, profiledFailMsg)
        
        if "verbose" in options: sepmsg()
        
        # run hpcstruct on test executable
        structPath = self.output.makePath("{}.hpcstruct".format(exeName))
        cmd = "{}/hpcstruct -o {} {} -I {} {}" \
            .format(self.hpctoolkitBinPath, structPath, self.hpcstructParams, self.testIncs, join(self.prefix.bin, split(self.yaml["run"]["cmd"])[0]))
        structTime, structFailMsg = self._execute(cmd, [], "hpcstruct", mpi=False, openmp=False)
        self._checkHpcstructExecution(structTime, structFailMsg, structPath)
    
        # run hpcprof on test measurements
        if profiledFailMsg or structFailMsg:
            infomsg("Skipping hpcprof execution because of previous failure")
        else:
            profPath = self.output.makePath("hpctoolkit-{}-database".format(exeName))
            cmd = "{}/hpcprof -o {} -S {} {} -I {} {}" \
                .format(self.hpctoolkitBinPath, profPath, structPath, self.hpcprofParams, self.testIncs, self.measurementsPath)
            profTime, profFailMsg = self._execute(cmd, [], "hpcprof", mpi=False, openmp=False)
            self._checkHpcprofExecution(profTime, profFailMsg, profPath)
    
        # let caller know if test case failed
        failed = normalFailMsg or profiledFailMsg or structFailMsg or profFailMsg
        
        if normalFailMsg:       failure, msg  = "NORMAL RUN FAILED", normalFailMsg
        elif profiledFailMsg:   failure, msg  = "HPCRUN FAILED",     profiledFailMsg
        elif structFailMsg:     failure, msg  = "HPCSTRUCT FAILED",  structFailMsg
        elif profFailMsg:       failure, msg  = "HPCPROF FAILED",    profFailMsg
        else:                   failure, msg  = None, None
        
        if failure:
            self.output.add("summary", "status", failure)
            self.output.add("summary", "status msg", msg)
            raise ExecuteFailed
            
    
    def _execute(self, cmd, keylist, label, profile=None, mpi=None, openmp=None, batch=None):

        import os
        from os.path import join
        import sys
        from spack.util.executable import ProcessError
        from spackle import execute
        from common import options, infomsg, verbosemsg, debugmsg, errormsg, sepmsg, ExecuteFailed
        
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
            cmd = "{}/hpcrun -o {} {} {}".format(self.hpctoolkitBinPath, self.measurementsPath, self.hpcrunParams, cmd)

        # ... add OpenMP parameters if wanted
        if wantOpenMP:
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
        #### timedCmd = "/usr/bin/time -f '%e\\t%S\\t%U' -o '{}/{}-time.txt' {}".format("OUT", label, cmd)
        timedCmd = "/usr/bin/time -f %e\\t%S\\t%U -o {} {}".format(timePath, cmd)
        self.output.add(label, "command", timedCmd, subroot=keylist)
        
        # execute the command
        verbosemsg("Executing {} test:\n{}".format(label, timedCmd))
        try:
            with open(outPath, "w") as outf:
                execute(timedCmd, cwd=runPath, env=env, output=outf, error=outf)
        except ProcessError as e:
            failed, msg = True, e.message
            infomsg("... {} execution failed: {}".format(label, msg))
        except Exception as e:
            fatalmsg("unexpected error attempting {} execution, {} ({})".format(label, e.message, type(e)))
            # does not return
        else:
            failed, msg = False, None
        
        # print test's output and cpu time
        if "verbose" in options:
            with open(outPath, "r") as f: print f.read()
        cputime = self._readTotalCpuTime(timePath)
        infomsg("... {} cpu time = {:<0.2f} seconds".format(label, cputime))
        
        # save results
        self.output.add(label, "cpu time", cputime, subroot=keylist)
        self.output.add(label, "status", "FAILED" if failed else "OK", subroot=keylist)
        self.output.add(label, "status msg", msg, subroot=keylist)
        
        return cputime, msg
    
    
    def _readTotalCpuTime(self, timePath):
            
        import csv
        from os.path import join
        
        with open(timePath, "r") as f:
            line = f.read()
            times = csv.reader([line], delimiter="\t").next()
        return float(times[1]) + float(times[2])


    def _checkTestResults(self):

        pass        # TODO
#       ... self.output.add("summary", "status", "CHECK FAILED")
#           self.output.add("summary", "status msg", xxx)
    

    def _writeInputs(self):

        import datetime

        now = datetime.datetime.now()
        self.output.add("input", "date", now.strftime("%Y-%m-%d %H:%M"))
        self.output.add("input", "test", self.testdir)
        self.output.add("input", "config spec", str(self.config))
        self.output.add("input", "spack spec", str(self.spec))
        self.output.add("input", "workspace", self.workspace.path)


    def _checkHpcrunExecution(self, normalTime, normalFailMsg, profiledTime, profiledFailMsg):
        
        from common import infomsg

        # compute profiling overhead
        if normalFailMsg or profiledFailMsg:
            infomsg("... hpcrun overhead not computed due to execution failure")
            self.output.add("run", "profiled", "hpcrun overhead %", "NA")
        else:
            overheadPercent = 100.0 * (profiledTime/normalTime - 1.0)
            infomsg("... hpcrun overhead = {:<0.2f} %".format(overheadPercent))
            self.output.add("run", "profiled", "hpcrun overhead %", overheadPercent)

        # summarize hpcrun log
        if profiledFailMsg:
            infomsg("... hpcrun log not summarized due to execution failure")
            self.output.add("run", "profiled", "hpcrun summary",  "NA")
        else:
            summaryDict = self._summarizeHpcrunLog()
            self.output.add("run", "profiled", "hpcrun summary", summaryDict)


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
            
        self.output.add("hpcstruct", "output checks", "FAILED" if msg else "OK")
        self.output.add("hpcstruct", "output msg",    msg)


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



