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
        
        from os.path import basename
        
        self.name      = basename(testdir)  # name of test case
        self.testdir   = testdir            # path to test case's directory
        self.config    = config             # Spack spec for desired build configuration
        self.workspace = workspace          # storage for collection of test job dirs

        # set up for per-test sub-logging
        ####self.log = xxx    # TODO


    def run(self):
        
        from common  import infomsg, errormsg
        from common  import BadTestDescription, PrepareFailed, BuildFailed, ExecuteFailed, CheckFailed

        infomsg("running test {} with config {}".format(self.testdir, self.config))
        
        try:
            
            self.yaml = self._readYaml()
            (srcdir, builddir, rundir) = self._prepareJobDir()
            self._buildTest(srcdir, builddir)
            self._runBuiltTest(builddir, rundir)
            self._checkTestResults(rundir)
            
        except BadTestDescription as e:
            msg = "missing or invalid '{}' file in test {}: {}".format("hpctest.yaml", self.testdir, e.args[0])
        except PrepareFailed as e:
            msg = "failed in setting up for building test {}: {}".format(self.testdir, e.args[0])
        except BuildFailed as e:
            msg = "failed in building test {}: {}".format(self.testdir, e.args[0])
        except ExecuteFailed as e:
            msg = "failed in excuting test {}: {}".format(self.testdir, e.args[0])
        except CheckFailed as e:
            msg = "failed in checking result of test {}: {}".format(self.testdir, e.args[0])
        else:
            msg = None
        
        if msg: errormsg(msg)


    def _readYaml(self):

        from os.path import join
        from spackle import loadYamlFile
        from common import BadTestDescription

        # read yaml file
        (yaml, error) = loadYamlFile( join(self.testdir, "hpctest.yaml") )
        if error:
            raise BadTestDescription(error)

        # validate and apply defaults
        # TODO
        
        return yaml
        

    def _prepareJobDir(self):

        from os import makedirs
        from os.path import basename, join
        from common import copyGlob

        # job directory
        jobdir = self.workspace.addJobDir(basename(self.testdir), self.config)
        
        # src directory -- immutable so just use teste's dir
        srcdir = self.testdir
        
        # build directory - make new or copy test's dir if not separable-build test
        # TODO: ensure relevant keys are in self.yaml, or handle missing keys here
        builddir = join(jobdir, "build");
        makedirs(builddir)
        if not "build" in self.yaml["build"]["separate"]:
            copyGlob(join(srcdir, "*"), builddir)
            
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

        import spack
        from spack.stage import DIYStage
        from common import assertmsg, options

        # get a spec for this test in specified configuration
        version = self.yaml["info"]["version"]
        specString = "{}@{}{}".format("tests." + self.name, version, self.config)
        print ">>>>>>>>> ", specString
        specs = spack.cmd.parse_specs(specString)
        assertmsg(len(specs) == 1, "'hpctest run' takes a single config spec.")
        spec = specs[0]
        spec.concretize()
   
        # build the package
        package = spack.repo.get(spec)
        package.stage = DIYStage(builddir)  # TODO: cf separable vs inseparable builds
        spack.do_checksum = False   # see spack.cmd.diy lines 91-92
        package.do_install(
            keep_prefix=False,
            install_deps=True,
            verbose="verbose" in options,
            keep_stage=True,        # don't remove source dir for DIY.
            dirty=True)             # TODO: cf separable vs inseparable builds


    def _runBuiltTest(self, builddir, rundir):

        pass        # TEMPORARY


    def _checkTestResults(self, rundir):

        pass        # TEMPORARY

        
        
