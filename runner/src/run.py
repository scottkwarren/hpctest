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
        
        import traceback
        from common  import infomsg, errormsg
        from common  import BadTestDescription, PrepareFailed, BuildFailed, ExecuteFailed, CheckFailed

        infomsg("running test {} with config {}".format(self.testdir, self.config))
        
        try:
            
            self._readYaml()
            (srcdir, builddir, rundir) = self._prepareJobDirs()
            self._buildTest(srcdir, builddir)
            self._runBuiltTest(builddir, rundir)
            self._checkTestResults(rundir)
            
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
            msg = "unexpected error {}".format(e.message)
        else:
            msg = None
        
        if msg: errormsg(msg)


    def _readYaml(self):

        import spack
        from common  import readYamlforTest, assertmsg

        self.yaml = readYamlforTest(self.testdir)
        self.name = self.yaml["info"]["name"]                    # name of test case

        # get a spec for this test in specified configuration
        version = self.yaml["info"]["version"]
        specString = "{}@{}{}".format("tests." + self.name, version, self.config)
        specs = spack.cmd.parse_specs(specString)
        assertmsg(len(specs) == 1, "'hpctest run' takes a single config spec.")     # TODO: check this earlier, once instead of per test
        self.spec = specs[0]
        self.spec.concretize()     # TODO: check that this succeeds


    def _prepareJobDirs(self):

        from os import makedirs, symlink
        from os.path import basename, join
        from shutil import copytree

        # job directory
        jobdir = self.workspace.addJobDir(self.name, self.config)
        
        # src directory -- immutable so just use teste's dir
        srcdir = self.testdir
        
        # build directory - make new or copy test's dir if not separable-build test
        # TODO: ensure relevant keys are in self.yaml, or handle missing keys here
        builddir = join(jobdir, "build");
        if "build" in self.yaml["build"]["separate"]:
            makedirs(builddir)
        else:
            copytree(srcdir, builddir)
            symlink( builddir, join(jobdir, basename(srcdir)) )
            
        # run directory - make new or use build dir if not separable-run test
        # TODO: ensure relevant keys are in self.yaml, or handle missing keys here
        if "run" in self.yaml["build"]["separate"]:
            rundir = join(jobdir, "run");
            makedirs(rundir)
        else:
            rundir = builddir
        
        # ...
        
        return (srcdir, builddir, rundir)


    def _buildTest(self, srcdir, builddir):

        import shutil
        import spack
        from spack.stage import DIYStage
        from spack.package import InstallError

        from common import options, BuildFailed

        # build the package if necessary
        self.package = spack.repo.get(self.spec)
        if not self.package.installed:
            self.package.stage = DIYStage(builddir)  # TODO: cf separable vs inseparable builds
            spack.do_checksum = False   # see spack.cmd.diy lines 91-92
            try:
                
                self.package.do_install(
                    keep_prefix=False,
                    install_deps=True,
                    verbose="verbose" in options,
                    keep_stage=True,        # don't remove source dir for DIY.
                    explicit=True,
                    dirty=True,             # TODO: cf separable vs inseparable builds
                    force=False)            # don't install if already installed -- TODO: deal with possibility that src may have changed
                
            except InstallError as e:
                errormsg(str(e))
                if not os.path.exists(e.pkg.build_log_path):
                    errormsg("...building produced no log.")
                else:
                    errormsg("...full build log written to stderr")
                    with open(e.pkg.build_log_path) as log:
                        shutil.copyfileobj(log, sys.stderr)
                raise BuildFailed
            except Exception as e:
                errormsg("during install, unexpected error {} ({})".format(e.message, e.args))
                raise BuildFailed
        

    def _runBuiltTest(self, builddir, rundir):

        from spackle import execute
        from common import infomsg, errormsg, ExecuteFailed
        
        # command to be executed, with profiling and launcher if needed
        # TODO: figure out what to do from options & package info
        if True:
            fullCmd = "/home/scott/hpctoolkit-current/hpctoolkit/INSTALL/bin/hpcrun -e REALTIME@10000 /projects/pkgs/mpich/bin/mpiexec -n 2 {}".format(self.yaml["run"]["cmd"])
        else:
            fullCmd = "/home/scott/hpctoolkit-current/hpctoolkit/INSTALL/bin/hpcrun -e REALTIME@10000 {}".format(self.yaml["run"]["cmd"])

        # execute the command
        try:
            
            infomsg("Executing test command:\n{}".format(fullCmd))
            execute(fullCmd, "", cwd=rundir, env={"OMP_NUM_THREADS":"2"} )
            ### execute(cmd, cwd=rundir)
            ### execute(cmd, cwd=rundir)
            ### execute(cmd, cwd=rundir)

        except Exception as e:
            msg = "unexpected error {}".format(e.message)
        else:
            msg = None
        
        if msg:
            errormsg(msg)
            raise ExecuteFailed


    def _checkTestResults(self, rundir):

        pass        # TEMPORARY
    
    


