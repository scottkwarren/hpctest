################################################################################
#                                                                              #
#  hpctest.py                                                                  #
#  top level class implementing functionality of HPCTest for programmatic use  #
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
##############################################################################


from os import environ, makedirs, system, rename
from os.path import dirname, join, normpath, realpath, expanduser, isdir, splitext
import sys
import common
import configuration, spackle, util


checksumName = ".checksum"


class HPCTest(object):


    #---------------------------#
    # Instance methods - public #
    #---------------------------#

    def __init__(self):
        
        global dimNames, dimDefaultMap, dimClassMap

        from common import infomsg, warnmsg, errormsg
        from dimension import TestDim, ConfigDim, HPCTkitDim, ProfileDim
                
        msgfunc = warnmsg if common.subcommand == "init" else errormsg if common.subcommand == "run" else None
        if (not common.hpctk_default) and msgfunc:
            msgfunc("no default HPCToolkit specified for profiling.\n"
                    "\n"
                    "To run profiling tests, specify '--hpctookit <path to bin dir>' on each 'hpctest run' command line.\n"
                    "To avoid specifying '--hpctoolkit' every time, do one of the following:\n"
                    "- edit hpctest/config.yaml to specify a default HPCToolkit path\n"
                    "- ensure that an HPCToolkit instance is on your $PATH to serve as default.\n"
                    "\n"
                    )
        
        # dimension info (requires paths and config to be set up)
        dimClasses    = [ TestDim, ConfigDim, HPCTkitDim, ProfileDim ]
        dimNames      = [ dim.name()                  for dim in dimClasses ]
        dimClassMap   = { dim.name() : dim            for dim in dimClasses }
        dimDefaultMap = { dim.name() : dim.default()  for dim in dimClasses }


    def init(self):
    
        # all the necessary work is done in __init__, so nothing here
        pass

        
    def run(self, argDimSpecs=dict(), args=dict(), numrepeats=1, reportspec="", sortKeys=[], studyPath=None, wantBatch=False):
        
        import common
        import configuration
        from executor   import Executor
        from study      import Study
        from iterate    import Iterate
        from report     import Report
        global dimNames, dimDefaultMap, dimClassMap
                
        # decode the dict of dimension strings into a complete dict of dimensionss, with default dims for missing dimensions
        dims = dict()
        for name in dimNames:
            spec = argDimSpecs[name] if name in argDimSpecs else dimDefaultMap[name]
            dims[name] = dimClassMap[name](spec) if spec else None # TODO: can't be None?
            
        # check preconditions and run tests if ok
        if dims["hpctoolkit"]:      # TODO: shouldn't require an HPCToolkit if no test wants profiling
            
            # run all the tests
            study = Study(studyPath if studyPath else common.workpath)
            if not wantBatch:
                wantBatch = configuration.get("config.batch.default", Executor.defaultToBackground())
            Iterate.doForAll(dims, args, numrepeats, study, wantBatch)
            print
            
            # report results
            reporter = Report()
            reporter.printReport(study, reportspec, sortKeys if len(sortKeys) else argDimSpecs.keys())
                
        else:
            # error message was printed during self._init_
            pass
         
        
    def report(self, studypath, reportspec="", sortKeys=[]):
        
        from os         import listdir
        from os.path    import join
        from common     import workpath, errormsg
        from report     import Report
        from study      import Study

        if not studypath:
            studies   = sorted(listdir(workpath), reverse=True)
            studypath = join(workpath, studies[0]) if len(studies) else None
        if studypath:
            if Study.isStudyDir(studypath):
                reporter  = Report()
                reporter.printReport(Study(studypath), reportspec, sortKeys)
            else:
                errormsg("path does not point to a study directory: {}".format(studypath))
        else:
            errormsg("no study to report on")
            


    def clean(self, workpath, tests, dependencies):
        
        from os        import listdir
        from os.path   import join
        import spackle        
        import common
        from common    import options, yesno, verbosemsg, debugmsg
        from study     import Study                                      

        def confirm(what):
            ask    = "Really delete all {}?".format(what)
            cancel = "Ok, will not delete them."
            return ("force" in options) or yesno(ask, cancel)
            
        # delete studies if desired
        if workpath and confirm("study directories"):
            if workpath == "<default>": workpath = common.workpath         ## TODO: pass None instead of "<default>" to keep command-line details out of here
            debugmsg("cleaning work directory {}".format(workpath))
            for name in listdir(workpath):
                path = join(workpath, name)
                if Study.isStudyDir(path): Study(path).clean()
        
        # uninstall tests if desired
        # BUG: "builtin" tests won't be uninstalled: not in 'tests' namespace,
        if tests and confirm("built tests"):
            verbosemsg("uninstalling built tests...")
            for name in sorted( spackle.allPackageNames("tests") ):
                if spackle.isInstalled(name):
                    spackle.uninstall(name)
                    verbosemsg("  uninstalled {} (all versions)".format(name))
            verbosemsg("...done")
        
        # uninstall dependencies if desired
        if dependencies and confirm("built dependencies"):
            verbosemsg("uninstalling built dependencies...")
            for name in sorted( spackle.allPackageNames("builtin") ):
                if spackle.isInstalled(name) and spackle.hasDependents(name):
                    # ... 'and' in case there's a 'builtin' w/ same name as a test
                    spackle.uninstall(name)
                    verbosemsg("  uninstalled {} (all versions)".format(name))
            verbosemsg("...done")

    
    
    def spack(self, cmdstring):
        
        import spackle
        spackle.do(cmdstring)


    def selftest(testspec="all", otherargs="", reportspec="", studyPath=None):
        
        import common
        from study      import Study
        from iterate    import Iterate
        from report     import Report
                
        infomsg("selftest not implemented")
        
#       # run tests, reporting results as we go
#       study = Study(studyPath if studyPath else common.workpath, prefix="selftest")
#       xxxxxxxxx
#       print
    

    #----------------------------#
    # Instance methods - private #
    #----------------------------#

    # support for deferred execution
    def _runOne(self, encodedArgs):
        
        from run import Run
        
        runArgs = Run.decodeInitArgs(encodedArgs) + (False, )  # + wantBatch
        runOb   = Run(*runArgs)
        runOb.run(echoStdout=False)

        
#    def miniapps(self):
#         
#    from os.path import join
#    import spack
#    from spack.repository import Repo
#    from common import own_spack_home
#         
#    # iterate over builtin packages
#    builtin = Repo(join(own_spack_home, "var", "spack", "repos", "builtin"))
#    for name in builtin.packages_with_tags("proxy-app"):
#        p = builtin.get(name)
#        print "name: " + p.name, "\n", "  homepage: " + p.homepage, "\n", "  url: " + (p.url if p.url else "None"), "\n"
    
    
    #---------------#
    # Class methods #
    #---------------#
    
    @classmethod
    def _ensureRepo(cls):
    
        import common
        import spackle
        
        # create new private repo for building test cases
        noRepo = spackle.getRepo("tests") is None
        if noRepo: spackle.createRepo("tests")
        HPCTest._ensureTests()
        if noRepo:
            spackle.addRepo(common.repopath)
        else:
            spackle.updateRepoPath(common.repopath)
    
        # extend external repo if one was specified
        pass
    
    
    @classmethod
    def _ensureTests(cls):
    
        from os.path import join, exists
        from common import options, repopath
        from test import Test
                
        def ensureOneTest(test):
                        
            # guards
            if "nochecksum" in options: return
            if not test.valid(): return
            if test.config() == "spack-builtin": return
            
            # check if repo has an up-to-date package for the test
            name = test.yamlName()
            packagePath = join(repopath, "packages", name)
            if exists(packagePath):
                needPackage = test.hasChanged()
            else:
                needPackage = True
                
            # if not, update package
            if needPackage:
                HPCTest._addPackageForTest(testDir, name)
                test.markUnchanged(testDir)
                
        Test.forEachDo(ensureOneTest)
    
    
    @classmethod
    def _addPackageForTest(cls, testPath, name):
        
        from os import mkdir
        from os.path import exists, join
        from shutil import copy, rmtree
        import spackle
        from common import debugmsg, repopath
        
        debugmsg("adding package for test {}".format(testPath))
        packagePath = join(repopath, "packages", name)
    
        # remove installed versions of package if any
        if exists(packagePath):
            cmd = "uninstall --all --force --yes-to-all {}".format(name)
            spackle.do(cmd, False)   # installed dependencies are not removed
        rmtree(packagePath, ignore_errors=True)
    
        # make package directory for this test
        mkdir(packagePath)
        
        # copy or generate test's description files
        hpath = join(testPath, "hpctest.yaml")
        ppath = join(testPath, "package.py")
        copy(hpath, packagePath)
        if exists(ppath):
            copy(ppath, packagePath)
        else:
           HPCTest._generatePackagePy(hpath, packagePath)
    
    
    @classmethod
    def _generatePackagePy(cls, hpath, ppath):
        
        # hpath => hpctest.yaml file to generate from
        # ppath => package directory to generate into
        
        from common import notimplemented
        notimplemented("HPCTest._generatePackagePy")


    

#########################
# MODULE INITIALIZATION #
#########################


# determine important paths
common.homepath = normpath( join(dirname(realpath(__file__)), "..", "..") )
_internalpath   = join(common.homepath, "internal")
common.own_spack_home = join(_internalpath, "spack")
common.own_spack_module_dir = join( common.own_spack_home, "lib", "spack" )
_whichHpcrun         = common.whichDir("hpcrun")
_hpctkLocal          = dirname(_whichHpcrun) if _whichHpcrun else None  # 'dirname' to get hpctoolkit install dir from 'bin' dir
common.hpctk_default = configuration.get("profile.hpctoolkit.path", _hpctkLocal)
common.hpctk_default = expanduser(common.hpctk_default) if common.hpctk_default else None
common.testspath     = join(common.homepath, "tests")
common.repopath      = join(_internalpath, "repos", "tests")
common.workpath      = join(common.homepath, "work")
if not isdir(common.workpath): makedirs(common.workpath)

# set up environment
environ["HPCTEST_HOME"] = common.homepath
sys.path[1:0] = [ common.own_spack_module_dir,
                  join(common.own_spack_module_dir, "external"),
                  join(common.own_spack_module_dir, "external", "yaml", "lib"),
                  join(common.own_spack_module_dir, "llnl"),
                ]

# set up local spack if necessary
if not isdir(common.own_spack_home):
    
    # inits to set up our own Spack, done only the first time HPCTest runs
    
    infomsg("Setting up internal Spack...")
    
    spack_version   = "0.11.2"
    spack_tarball   = join(_internalpath, "spack-{}.tar.gz".format(spack_version))
    spack_extracted = join(_internalpath, "spack-{}".format(spack_version))
    spack_dest      = join(_internalpath, "spack")
    system("cd {}; tar xzf {}".format(_internalpath, spack_tarball))
    rename(spack_extracted, spack_dest)

    infomsg("Spack found these compilers automatically:")
    spackle.do("compilers")
    infomsg("To add more existing compilers or build new ones, use 'hpctest spack <spack-cmd>' and")
    infomsg("see 'Getting Started / Compiler configuration' at spack.readthedocs.io.\n")
spackle.initSpack()     # must be done at each execution of our Spack

# set up configuration system
configuration.initConfig()    # must come after paths, spack, and environ are initialized

# set up private repo
HPCTest._ensureRepo()






