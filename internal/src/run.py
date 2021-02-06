################################################################################
#                                                                              #
#  run.py                                                                      #
#  run a single test case in a new run directory in given study                #
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




from hpctest import HPCTest


class Run(object):


    # batch job submission
    from executor import Executor
    executor = Executor.localExecutor()


    # public operation parameter types
    class ProfileParams(object):
        def __init__(self):
            binPath = ""        # location of the HPCToolkit installation to use
            params  = ""        # profiling params for 'hpcrun'
            outPath = ""        # where to put 'hpcrun' measurements file

    
    # METHODS
    
    def __init__(self, test, build, hpctoolkit, profile, numrepeats, study, wantBatch):
        
        from os.path import basename, join

        # general params
        self.test        = test
        self.build       = build                          # Spack spec for desired build configuration
        self.study       = study                          # storage for collection of test run dirs

        # hpctoolkit params
        self.hpctoolkit        = hpctoolkit
        self.hpctoolkitBinPath = join(hpctoolkit, "bin")
        self.profile           = profile
        self.testIncs          = "./+"

        # execution params
        self.numrepeats = numrepeats
    
    
    def description(self, forName=False):
        
        from os.path import basename
        return self.test.description(self.build, self.hpctoolkitBinPath, self.profile, forName=forName)
    
    
    def run(self, echoStdout=True):
        
        from os.path import join, relpath
        import time
        import common
        from common import args, homepath, infomsg, sepmsg
        from common import HPCTestError, BadTestDescription, BadBuildSpec, PrepareFailed, BuildFailed, ExecuteFailed, CheckFailed
        from experiment import Experiment
        from experiment.profileExperiment import ProfileExperiment
        from util.tee import StdoutTee, StderrTee
                
        # job directory
        self.jobdir = self.study.addRunDir(self.description(forName=True))
        self.output = self.study.addResultDir(self.jobdir, "OUT")
        self._writeInputs()
        
        # save console output in OUT directory
        outPath = self.output.makePath("console-output.txt")
        filter  = (lambda s: s) if echoStdout else (lambda s: None)
        with StdoutTee(outPath, stream_filters=[filter]), StderrTee(outPath, stream_filters=[filter]):
            
            startTime = time.time()
            
            sepmsg(True)
            gerundive = "running"   if args["run"]   else \
                        "building"  if args["build"] else \
                        "debugging" if args["debug"] else \
                        "running"   # selftest => running
            infomsg( "{} test {}".format(gerundive, self.description()) )
            sepmsg(True)
            
            # run the test
            try:
                
                self._examineYaml()
                self._buildTest()
                
                if not common.args["build"]:    # ie not build-only
                    self.experiment = ProfileExperiment(self.test, self, self.output,
                                                        self.build, self.hpctoolkit, self.profile)
                    self.experiment.run()
                    self.output.addSummaryStatus("OK", None)
                
            except BadTestDescription as e:
                msg = "missing or invalid '{}' file: {}".format("hpctest.yaml", e.message)
            except BadBuildSpec as e:
                msg = "build spec invalid per Spack ('{}'):\n{}".format(self.spec, e.message)
            except PrepareFailed as e:
                msg = "setup for test build failed"
            except BuildFailed as e:
                msg = "test build failed"
            except ExecuteFailed as e:
                msg = "test execution failed"
            except CheckFailed as e:
                msg = "test result check failed"
            except HPCTestError as e:
                msg = e.message
            except Exception as e:
                msg = "unexpected error: {} ({})".format(e.message, type(e).__name__)
            else:
                msg = None
                
            if msg: infomsg(msg)
            
            # finish writing results
            elapsedTime = time.time() - startTime
            self._addMissingOutputs()
            self.output.add("summary", "elapsed time", elapsedTime, format="{:0.2f}")
            self.output.write()


    def _examineYaml(self):

        from common import BadTestDescription
        
        msg = self.test.yamlErrorMsg()
        if msg:
            self.wantProfiling = False  # trouble later if missing
            self.output.add("input", "wantProfiling", "False")
            self.output.addSummaryStatus("READING YAML FAILED", self.test.yamlErrorMsg())
            raise BadTestDescription(msg)
        else:
            self.wantProfiling = self.test.wantProfile()
            self.output.add("input", "wantProfiling", str(self.wantProfiling))


    def _makeBuildSpec(self):

        import spackle
        from common import BadBuildSpec
        
        namespace = "builtin" if self.test.builtin() else "tests"
        spackString = "{}@{}{}".format(namespace + "." + self.test.name(), self.test.version(), self.build)
        self.spec = spackString  ## NOTE: so after bad-spec exception 'self.spec' can be used in error msg
        self.output.add("input", "spack spec", str(self.spec))


    def _prepareJobDirs(self):

        from os import symlink
        from os.path import basename, join
        from shutil import copytree
        from common import PrepareFailed

        try:

            # src directory -- immutable so just use test's dir
            self.srcdir = self.test.path()
            
            # build directory -- copy test's dir if not separable-build test
            self.builddir = join(self.jobdir, "build");
            copytree(self.srcdir, self.builddir)
            symlink( self.builddir, join(self.jobdir, basename(self.srcdir)) )
                
            # run directory - use build dir if not separable-run test
            self.rundir = self.builddir
                
        except Exception as e:
            self.output.addSummaryStatus("PREPARE FAILED", e.message)
            raise PrepareFailed(e.message)
        

    def _buildTest(self):

        import os
        from os.path import basename, join, isfile
        from shutil import copyfile
        from sys import stdout
        from util.tee import StdoutTee, StderrTee
        from common import escape
        import spackle

        from common import options, infomsg, errormsg, fatalmsg, BuildFailed, ElapsedTimer

        self._makeBuildSpec()
        self._prepareJobDirs()

        # build the package if necessary
        try:
                        
            buildTime = 0.0     # here in case 'isSpecInstalled' raises an exception
            
            # 'always' => build every time, but never actually install
            # don't actually install b/c Spack treats every 'dev-build' as different,
            #   so installed instances just pile up
            always = self.test.buildAlways()
            
            if spackle.isSpecInstalled(self.spec) and not always:
                
                if "verbose" in options: infomsg("skipping build, test already installed")
                status, msg = "OK", "already built"
                self.packagePrefix = spackle.specPrefix(self.spec)

                # make alias(es) in build dir to product(s) in existing install dir
                productRelPaths = self.test.installProducts()
                for relpath in productRelPaths:
                    productName    = basename(relpath)
                    buildPath      = join(self.rundir, relpath)
                    installPath    = join(self.packagePrefix, productName)
                    installBinPath = join(self.packagePrefix, "bin", productName)
                    if isfile(installPath):
                        copyfile(installPath, buildPath)
                    if isfile(installBinPath):
                        copyfile(installBinPath, buildPath)

            else:
                
                outPath = self.output.makePath("{}-output.txt", "build")
                filter  = (lambda s: s) if "verbose" in options else (lambda s: None)
                with StdoutTee(outPath, stream_filters=[filter]), StderrTee(outPath, stream_filters=[filter]):
                    with ElapsedTimer() as t:
                        
                        srcDir = self.builddir if not self.test.builtin() else None
                        spackle.installSpec(self.spec, srcDir, always)
                        status, msg = "OK", None
                        self.packagePrefix = spackle.specPrefix(self.spec)
                
                        # make alias(es) in install dir to product(s) in build dir
                        productRelPaths = self.test.installProducts()
                        for relpath in productRelPaths:
                            productName    = basename(relpath)
                            buildPath      = join(self.rundir, relpath)
                            installPath    = join(self.packagePrefix, productName)
                            installBinPath = join(self.packagePrefix, "bin", productName)
                            if not isfile(installPath) \
                               and not isfile(installBinPath):
                                copyfile(buildPath, installBinPath)
        
                        buildTime = t.secs
                        
        except Exception as e:
            status, msg =  "FAILED", e.message
            self.packagePrefix = None

        # save results
        cmd = "cd {}; cp spack-build* > {} 2>&1 /dev/null".format(self.builddir, self.output.getDir())
        os.system(escape(cmd))
        self.output.add("build", "prefix",     self.packagePrefix)
        self.output.add("build", "cpu time",   buildTime, format="{:0.2f}")
        self.output.add("build", "status",     status)
        self.output.add("build", "status msg", msg)

        # finish up
        if status == "OK":
            infomsg("build time = {:<0.2f} seconds".format(buildTime))
        else:
            if status == "FATAL":
                fatalmsg(msg)
            else:
                errormsg("build failed, " + msg)
                if "verbose" in options:
                    try:
                        logPath = e.pkg.build_log_path
                    except:
                        logPath = None
                    if logPath:
                        infomsg("...build log:")
                        with open(e.pkg.build_log_path) as log:
                            copyfileobj(log, stdout)
                    else:
                        infomsg("...build produced no log.")
            self.output.addSummaryStatus("BUILD FAILED", msg)
            raise BuildFailed(msg)

    
    def _writeInputs(self):

        from collections import OrderedDict
        import datetime
        from os.path import join, relpath
        from common import homepath

        now = datetime.datetime.now()
        self.output.add("input", "date",              now.strftime("%Y-%m-%d %H:%M"))
        self.output.add("input", "test",              self.test.relpath())
        self.output.add("input", "build spec",        str(self.build))
        self.output.add("input", "hpctoolkit",        str(self.hpctoolkitBinPath))
        self.output.add("input", "hpctoolkit params", self.profile._asdict())
        self.output.add("input", "num repeats",       self.numrepeats)
        self.output.add("input", "study dir",         self.study.path)


    def _addMissingOutputs(self):
        
        if "build" not in self.output.get():
            self.output.add("build", "NA")
        if "run" not in self.output.get():
            self.output.add("run", "NA")
        if "wantProfiling" not in self.output.get("input"):
            self.output.add("input", "wantProfiling", "False")
        if self.wantProfiling and self.output.get("run") != "NA":   ## TODO: 'wantProfiling' WANKS IF THERE WAS NO YAML FILE
            if "hpcstruct" not in self.output.get("run", "profiled"):
                self.output.add("run", "hpcstruct", "NA")
            if "hpcprof" not in self.output.get("run", "profiled"):
                self.output.add("run", "hpcprof", "NA")


#==========================


    def execute(self, cmd, subroot, label, mpi, openmp):

        import os
        from os.path import join
        import sys
        from subprocess import CalledProcessError
        from common import options, escape, infomsg, verbosemsg, sepmsg
        from common import HPCTestError, ExecuteFailed
        from spackle import mpiPrefix
        from run import Run
        
        # compute command to be executed
        # ... start with test's run command
        binPath   = join(self.packagePrefix, "bin")
        runSubdir = self.test.runSubdir()
        runPath   = join(self.rundir, runSubdir) if runSubdir else self.rundir
        outPath   = self.output.makePath("{}-output.txt", label)
        timePath  = self.output.makePath("{}-time.txt", label)

        # ... OpenMP parameters if wanted
        if openmp:
            threads = self.test.numThreads()
        else:
            threads = 0

        # ... MPI launching code if wanted
        if mpi:
            ranks = self.test.numRanks()
            mpipath = join(mpiPrefix(self.spec), "bin")
        else:
            ranks = 0       # tells executor.wrap not to use MPI
            mpipath = None
        
        # ... let executor add code immediately surrounding cmd 
        cmd = Run.executor.wrap(cmd, runPath, binPath, ranks, threads, spackMPIBin=mpipath)
        
        # ... always add resource limiting code
        limitstring = self._makeLimitString()
        cmd = "/bin/bash -c \"ulimit {}; {}\" ".format(limitstring, escape(cmd))
        
        # ... always add timing code
        cmd = "/usr/bin/time -f \"%e %S %U\" -o {} {}".format(timePath, cmd)
        
        self.output.add(label, "command", cmd, subroot=subroot)
            
        # execute the command
        verbosemsg("Executing {} test:\n{}".format(label, cmd))
        msg = None  # for cpu-time messaging below
        try:
            
             Run.executor.run(cmd, runPath, binPath, ranks, threads, outPath, self.description())
                
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
                 
                # compute effective limit accordingly
                value = str( int(value) * multiplier )
 
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




##########################################
# BATCH EXECUTION                        #
##########################################


    @classmethod
    def submitJob(cls, test, build, hpctoolkit, profile, numrepeats, study):   # returns jobID, out, err
        
        import os
        from os.path import join
        from common import optionsArgString, homepath
        import configuration
        
        optString = optionsArgString()
        initArgs  = Run._encodeInitArgs(test, build, hpctoolkit, profile, numrepeats, study)
        cmd = "{}/hpctest _runOne {} '{}'; exit 0".format(homepath, optString, initArgs)        
        prelude = configuration.get("config.batch.prelude", [])
        numRanks = test.numRanks()
        numThreads = test.numThreads()
        name = test.name()
        desc = test.description(build, hpctoolkit, profile, forName=False)
        jobID, out, err = Run.executor.submitJob(cmd, prelude, numRanks, numThreads, name, desc)
        
        return jobID, out, err
    
    
    @classmethod
    def descriptionForJob(cls, jobID):
    
        return Run.executor.description(jobID)
    
    
    @classmethod
    def isFinished(cls, jobID):
        
        return Run.executor.isFinished(jobID)
    
    
    @classmethod
    def waitFinished(cls, jobID):
        
        Run.executor.waitFinished(jobID)
    
    
    @classmethod
    def pollForFinishedJobs(cls):

        return Run.executor.pollForFinishedJobs()
    
    
    @classmethod
    def _encodeInitArgs(cls, test, build, hpctoolkit, profile, numrepeats, study):
        
        from os.path import basename
        import common
        
        verb = "build" if common.args["build"] else \
               "run"   if common.args["run"]   else \
               "debug" if common.args["debug"] else None
        encodedArgs = "!".join([verb, test.path(), build, hpctoolkit,
                                profile.hpcrun, profile.hpcstruct, profile.hpcprof,
                                str(numrepeats), study.path])
        encodedArgs = encodedArgs.replace(" ", "#")
        
        return common.magic_cookie + encodedArgs
    
    
    @classmethod
    def decodeInitArgs(cls, encodedArgs):
        
        import common
        from common import magic_cookie
        from sys import exit
        from dimension.profileDim import ProfileArgs
        from study import Study
        from test import Test
        
        if encodedArgs.startswith(magic_cookie):
            
            encodedArgs = encodedArgs.replace(magic_cookie, "")
            
            encodedArgs = encodedArgs.replace("#", " ")
            argStrings = encodedArgs.split("!")
            
            verb, testdir, build, hpctoolkit = argStrings[0:4]
            profile = ProfileArgs(*argStrings[4:7])
            numrepeats = int(argStrings[7])
            study = Study(argStrings[8])
            
            common.args[verb] = True
            return (Test(testdir), build, hpctoolkit, profile, numrepeats, study)
        
        else:
            print "The _runOne command is for internal use only."
            exit()



