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


class Run():


    # batch job submission
    from executor import Executor
    executor = Executor.localExecutor()

    
    def __init__(self, test, config, hpctoolkit, profile, numrepeats, study, wantBatch):
        
        from os.path import basename, join

        # general params
        self.test        = test
        self.config      = config                         # Spack spec for desired build configuration
        self.study       = study                          # storage for collection of test run dirs

        # hpctoolkit params
        self.hpctoolkit        = hpctoolkit
        self.hpctoolkitBinPath = join(hpctoolkit, "bin")
        self.hpctoolkitParams  = profile.strip(" ;:").replace(";", ":")
        paramList = self.hpctoolkitParams.split(":")
        self.hpcrunParams      = paramList[0]
        self.hpcstructParams   = paramList[1] if len(paramList) >= 2 else ""
        self.hpcprofParams     = paramList[2] if len(paramList) >= 3 else ""
        self.testIncs          = "./+"

        # execution params
        self.numrepeats = numrepeats
    
    
    def description(self, forName=False):
        
        from os.path import basename
        return self.test.description(self.config,
                                     self.hpctoolkitBinPath,
                                     self.hpctoolkitParams,
                                     forName=forName)
    
    
    def run(self, echoStdout=True):
        
        from os.path import join, relpath
        import time
        from common import homepath, infomsg, sepmsg
        from common import BadTestDescription, BadBuildSpec, PrepareFailed, BuildFailed, ExecuteFailed, CheckFailed
        from experiment import Experiment
        from llnl.util.tty.log import log_output
                
        # job directory
        self.jobdir = self.study.addRunDir(self.description(forName=True))
        self.output = self.study.addResultDir(self.jobdir, "OUT")
        self._writeInputs()
        
        # save console output in OUT directory
        outPath = self.output.makePath("console-output.txt")
        with log_output(outPath, echo=echoStdout):
            
            startTime = time.time()
            self.hpcrunParams.replace(" ", ".")
            
            sepmsg(True)
            infomsg( "running test {}".format(self.description()) )
            sepmsg(True)
            
            try:
                
                # build the test case
                self._examineYaml()
                self._makeBuildSpec()
                self._prepareJobDirs()
                self._buildTest()
                
                # use an experiment instance to perform one run
                cmd        = self.test.cmd()
                mpiPrefix  = self.spec["mpi"].prefix if "+mpi" in self.spec else None
                runSubdir  = self.test.runSubdir()
                numRanks   = self.test.numRanks()
                numThreads = self.test.numThreads()
                wantMPI    = "+mpi" in self.spec
                wantOMP    = "+openmp" in self.spec
                self.experiment =  \
                    Experiment(cmd, self.package.prefix, mpiPrefix, self.rundir, runSubdir,
                               numRanks, numThreads, wantMPI, wantOMP,
                               self.config, self.hpctoolkit, self.hpctoolkitParams, self.wantProfiling,
                               self.output)
                self.experiment.run()
                
                self.output.addSummaryStatus("OK", None)
                
            except BadTestDescription as e:
                msg = "missing or invalid '{}' file: {}".format("hpctest.yaml", e.message)
            except BadBuildSpec as e:
                msg = "build spec invalid per Spack ({}):\n{}".format(self.spec, e.message)
            except PrepareFailed as e:
                msg = "setup for test build failed"
            except BuildFailed as e:
                msg = "test build failed"
            except ExecuteFailed as e:
                msg = "test execution failed"
            except CheckFailed as e:
                msg = "test result check failed"
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
        
        if self.test.yamlErrorMsg():
            self.wantProfiling = False  # trouble later if missing
            self.output.add("input", "wantProfiling", "False")
            self.output.addSummaryStatus("READING YAML FAILED", self.test.yamlErrorMsg())
            raise BadTestDescription(msg)
        else:
            self.version = self.test.version()  # TODO: let 'info.version' be missing, and use package default in such cases
            self.builtin = self.test.builtin()
            self.wantProfiling = self.test.profile()
            self.output.add("input", "wantProfiling", str(self.wantProfiling))


    def _makeBuildSpec(self):

        import spackle
        from common import BadBuildSpec
        
        namespace = "builtin" if self.builtin else "tests"
        spackString = "{}@{}{}".format(namespace + "." + self.test.yamlName(), self.version, self.config)
        try:
            
            self.spec = spackle.parseSpec(spackString)[0]                # TODO: deal better with possibility that returned list length != 1
            self.output.add("input", "spack spec", str(self.spec))
            if "+mpi" in self.spec:
                spackString += " +mpi"
                self.spec = spackle.parseSpec(spackString)[0]            # TODO: deal better with possibility that returned list length != 1
            if "+openmp" in self.spec:
                spackString += " +openmp"
                self.spec = spackle.parseSpec(spackString)[0]            # TODO: deal better with possibility that returned list length != 1
            spackle.concretizeSpec(self.spec)
            
        except Exception as e:
            self.output.addSummaryStatus("CONFIG INVALID", e.message)
            raise BadBuildSpec(e.message)


    def _prepareJobDirs(self):

        from os import makedirs, symlink
        from os.path import basename, join
        from shutil import copytree
        from common import PrepareFailed

        try:

            # src directory -- immutable so just use test's dir
            self.srcdir = self.test.path()
            
            # build directory -- make new or copy test's dir if not separable-build test
            self.builddir = join(self.jobdir, "build");
            separate = self.test.yaml("build.separate")
            if "build" in separate:
                makedirs(self.builddir)
            else:
                copytree(self.srcdir, self.builddir)
                symlink( self.builddir, join(self.jobdir, basename(self.srcdir)) )
                
            # run directory - make new or use build dir if not separable-run test
            if "run" in separate:
                self.rundir = join(self.jobdir, "run");
                makedirs(self.rundir)
            else:
                self.rundir = self.builddir
                
        except Exception as e:
            self.output.addSummaryStatus("SETUP FAILED", e.message)
            raise PrepareFailed(e.message)
        

    def _buildTest(self):

        import os
        from os.path import basename, join, isfile
        from shutil import copyfileobj
        from sys import stdout
        from llnl.util.tty.log import log_output
        from common import escape
        import spackle

        from common import options, infomsg, errormsg, fatalmsg, BuildFailed, ElapsedTimer

        # build the package if necessary
        self.package = spackle.packageFromSpec(self.spec)
        if self.package.installed:
            if "verbose" in options: infomsg("skipping build, test already installed")
            status, msg = "OK", "already built"
            buildTime = 0.0
        else:
            if not self.builtin:
                spackle.setDIY(self.package, self.builddir)     # TODO: cf separable vs inseparable builds
            
            outputPath = self.output.makePath("{}-output.txt", "build")
            with log_output(outputPath, echo="verbose" in options):
                with ElapsedTimer() as t:
                    
                    try:
                        self.package.do_install(
                            restage=True,
                            keep_prefix=False,
                            install_deps=True,
                            verbose="verbose" in options,
                            keep_stage=True,        # don't remove source dir for DIY.
                            explicit=True,
                            dirty=True,             # TODO: cf separable vs inseparable builds
                            force=False)            # don't install if already installed -- TODO: deal with possibility that src may have changed
                        status, msg = "OK", None
                    except Exception as e:
                        status, msg =  "FAILED", e.message
                    except BaseException as e:
                        print "unexpected error: {}".format(e.message)
                        
                    buildTime = t.secs
        
        # make alias(es) in build directory to the built product(s)
        products = self.test.installProducts()
        self.prefix = self.package.prefix      # prefix path is valid even if package failed to install
        for productRelpath in products:
            productPath = join(self.rundir, productRelpath)
            productName = basename(productPath)
            productPrefix = join(self.prefix.bin, productName)
            if not isfile(productPath):
                os.symlink(productPrefix, productPath)
            
        # save results
        cmd = "cd {}; cp spack-build.* {} > /dev/null 2>&1".format(self.builddir, self.output.getDir())
        os.system(escape(cmd))
        self.output.add("build", "prefix",     str(self.prefix))
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
                    if not os.path.exists(e.pkg.build_log_path):
                        infomsg("...build produced no log.")
                    else:
                        infomsg("...build log:")
                        with open(e.pkg.build_log_path) as log:
                            copyfileobj(log, stdout)
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
        self.output.add("input", "config spec",       str(self.config))
        self.output.add("input", "hpctoolkit",        str(self.hpctoolkitBinPath))
        self.output.add("input", "hpctoolkit params", OrderedDict({"hpcrun":self.hpcrunParams, "hpcstruct":self.hpcstructParams, "hpcprof":self.hpcprofParams}))
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
            if "hpcstruct" not in self.output.get("run"):
                self.output.add("run", "hpcstruct", "NA")
            if "hpcprof" not in self.output.get("run"):
                self.output.add("run", "hpcprof", "NA")



   
##########################################
# SUPPORT FOR BATCH EXECUTION            #
##########################################


    @classmethod
    def submitJob(cls, test, config, hpctoolkit, profile, numrepeats, study):   # returns jobID, out, err
        
        import os
        from os.path import join
        from common import homepath
        
        optString = Run._makeOptionsArgString()
        initArgs  = Run._encodeInitArgs(test, config, hpctoolkit, profile, numrepeats, study)
        cmd = "{}/hpctest _runOne {} '{}'; exit 0".format(homepath, optString, initArgs)
        env = os.environ.copy()
        numRanks = test.numRanks()
        numThreads = test.numThreads()
        name = test.description(config, hpctoolkit, profile, forName=True)
        desc = test.description(config, hpctoolkit, profile, forName=False)
        jobID, out, err = Run.executor.submitJob(cmd, env, numRanks, numThreads, None, name, desc)
        
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
    def _makeOptionsArgString(cls, options=None):
        
        import common
        if not options: options = common.options
        
        optString = ""
        if "verbose"    in options:    optString += " --verbose"
        if "debug"      in options:    optString += " --debug"
        if "force"      in options:    optString += " --force"
        if "traceback"  in options:    optString += " --traceback"
        
        return optString
    
    
    @classmethod
    def _encodeInitArgs(cls, test, config, hpctoolkit, profile, numrepeats, study):
        
        from os.path import basename
        
        encodedArgs = ",".join([test.path(), config, hpctoolkit, profile, str(numrepeats), study.path])
        encodedArgs = encodedArgs.replace(" ", "#")
        return encodedArgs
    
    
    @classmethod
    def decodeInitArgs(cls, encodedArgs):
        
        from study import Study
        from test import Test
        
        encodedArgs = encodedArgs.replace("#", " ")
        argStrings = encodedArgs.split(",")
        
        testdir, config, hpctoolkit, profile = argStrings[:3+1]
        numrepeats = int(argStrings[4])
        study = Study(argStrings[5])
        
        return (Test(testdir), config, hpctoolkit, profile, numrepeats, study)



