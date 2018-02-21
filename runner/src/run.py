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
        
        self.testdir   = testdir                # path to test case's directory
        self.config    = config                 # Spack spec for desired build configuration
        self.workspace = workspace              # storage for collection of test job dirs

        # set up for per-test sub-logging
        ####self.log = xxx    # TODO


    def run(self):
        
        from common import infomsg, errormsg, sepmsg
        from common import BadTestDescription, PrepareFailed, BuildFailed, ExecuteFailed, CheckFailed
        
        sepmsg(True)
        infomsg("running test {} with config {}".format(self.testdir, self.config))
        sepmsg(True)
        
        try:
            
            self._readYaml()
            self._prepareJobDirs()
            self._buildTest()
            self._runBuiltTest()
            self._checkTestResults()
            
        except BadTestDescription as e:
            msg = "missing or invalid '{}' file in test {}".format("hpctest.yaml", self.testdir)
        except PrepareFailed as e:
            msg = "failed in setting up for building test {}".format(self.testdir)
        except BuildFailed as e:
            msg = "failed to build test {}".format(self.testdir)
        except ExecuteFailed as e:
            msg = "failed to execute test {}".format(self.testdir)
        except CheckFailed as e:
            msg = "failed in checking result of test {}".format(self.testdir)
        except Exception as e:
            msg = "unexpected error in test {} - {} ({})".format(self.testdir, type(e).__name__, e.message)
        else:
            msg = None
        
        if msg: errormsg(msg)
        self.output.save()



    def _readYaml(self):

        import spack
        from common  import readYamlforTest, assertmsg

        self.yaml = readYamlforTest(self.testdir)
        self.name = self.yaml["info"]["name"]                    # name of test case

        # get a spec for this test in specified configuration
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
        from output import Output

        # job directory
        self.jobdir = self.workspace.addJobDir(self.name, self.config)
        
         # storage for hpctest inputs and outputs
        self.inputdir = join(self.jobdir, "_IN")
        makedirs(self.inputdir)
        self._writeInputs()
        self.output = Output(self.jobdir)

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
            self.output.add("build", "status", status)
            self.output.add("build", "status msg", msg)

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
                    raise BuildFailed


    def _runBuiltTest(self):

        from os import mkdir
        from os.path import join, isdir
        from common import infomsg, sepmsg

        # execute test case with and without profiling (to measure overhead)
        cmd = self.yaml["run"]["cmd"]
        exeName = cmd.split()[0]
        self.measurementsPath = self.output.makePath("hpctoolkit-{}-measurements".format(exeName))
        
        try:
            normalTime = self._executeWithMods("normal", False)
        except ExecuteFailed:
            self.outout.add("run", "normal", "status",  "FAILED")
            infomsg("... normal execution failed: {}".format(xxx))
            raise
        else:
            infomsg("... normal cpu time = {:<0.2f} seconds".format(normalTime))
            self.output.add("run", "normal", "status", "OK")
            self.output.add("run", "normal", "cpu time",  normalTime)
            
        try:
            profiledTime = self._executeWithMods("profiled", True)
        except ExecuteFailed:
            infomsg("... profiled execution failed: {}".format(xxx))
            self.output.add("run", "profiled", "status",  "FAILED")
            raise
        else:
            infomsg("... profiled cpu time = {:<0.2f} seconds".format(profiledTime))
            self.output.add("run", "profiled", "status",  "OK")
            self.output.add("run", "profiled", "cpu time", profiledTime)
        sepmsg()
        
        # compute profiling overhead
        overheadPercent = 100.0 * (profiledTime/normalTime - 1.0)
        infomsg("...hpcrun overhead = {} %".format(overheadPercent))

        # summarize hpcrun log
        summaryDict = self._summarizeHpcrunLog()
        
        # save results
        self.output.add("run", "profiled", "status",            "OK")
        self.output.add("run", "profiled", "cpu time",          profiledTime)
        self.output.add("run", "profiled", "hpcrun overhead %", overheadPercent)
        self.output.add("run", "profiled", "hpcrun summary",    summaryDict)


    def _executeWithMods(self, label, wantProfile):

        import os
        from os.path import join
        import sys
        from spackle import execute
        from common import options, infomsg, verbosemsg, errormsg, sepmsg, ExecuteFailed
        
        cmd         = self.yaml["run"]["cmd"]
        wantMPI     = '+mpi' in self.spec
        wantOpenMP  = '+openmp' in self.spec
        wantBatch   = False     # TODO: figure out from options & package info

        # compute command to be executed
        # ... start with test's run command
        env = os.environ.copy()         # necessary b/c execute's (subprocess.Popen's) 'env' arg, if given, discards existing os environment
        env["PATH"] = self.package.prefix + "/bin" + ":" + env["PATH"]
        runPath  = self.rundir if "dir" not in self.yaml["run"] else join(self.rundir, self.yaml["run"]["dir"])
        outPath  = self.output.makePath("{}-output.txt", label)
        timePath = self.output.makePath("{}-time.txt", label)
        
        # ... add profiling code if wanted
        if wantProfile:
            toolkitBinPath   = "/home/scott/hpctoolkit-current/hpctoolkit/INSTALL/bin"
            toolkitRunParams = "-e REALTIME@10000"
            cmd = "{}/hpcrun -o {} {} {}".format(toolkitBinPath, self.measurementsPath, toolkitRunParams, cmd)

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
        
        # execute the command
        infomsg("Executing {} command:\n{}".format(label, timedCmd))
        verbosemsg("... with env:\n{}".format(env))
        try:
            
            with open(outPath, "w") as outf:
                execute(timedCmd, cwd=runPath, env=env, output=outf, error=outf)
            
        except Exception as e:
            msg = "command produced error {}".format(e.message)
        except Exception as e:
            fatalmsg("unexpected error {} ({})".format(e.message, type(e)))
        else:
            msg = None

        # send command's output to stdout if verbose
        if "verbose" in options:
            with open(outPath, "r") as f:
                print f.read()
        
        if msg:
####        self.output.add("run", label, "xxx", xxx)
            errormsg(msg)
            raise ExecuteFailed
            
        return self._readTotalCpuTime(timePath)
    
    
    def _readTotalCpuTime(self, timePath):
            
        import csv
        from os.path import join
        
        with open(timePath, "r") as f:
            line = f.read()
            times = csv.reader([line], delimiter="\t").next()
        return float(times[1]) + float(times[2])


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


    def _checkTestResults(self):

        pass        # TODO
    

    def _writeInputs(self):

        pass


    


