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
                
        if (not common.hpctk_default):
            warnmsg("no default HPCToolkit specified for profiling.\n"
                    "\n"
                    "To run profiling tests, specify '--hpctookit <path to install directory>' on each 'hpctest run' command line.\n"
                    "To avoid specifying '--hpctoolkit' every time, do one of the following:\n"
                    "- edit hpctest/config.yaml and set profile.hpctoolkit.path to desired default HPCToolkit install directory\n"
                    "- or ensure that an HPCToolkit bin directory is on your $PATH.\n"
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

        
    def run(self, argDimSpecs=dict(), numrepeats=1, reportspec="", sortKeys=[], studyPath=None, wantBatch=False):
        
        import common
        import configuration
        from executor   import Executor
        from study      import Study
        from iterate    import Iterate
        from report     import Report
        global dimNames, dimDefaultMap, dimClassMap
                
        # decode the dict of dimension strings into a complete dict of dimensions, with default dims for missing dimensions
        dims = dict()
        for name in dimNames:
            spec = argDimSpecs[name] if name in argDimSpecs else dimDefaultMap[name]
            dims[name] = dimClassMap[name](spec)
            
        # check preconditions and run tests if ok
        # FIXME: 'dims["hpctoolkit"]' does not test whether any paths were specified!!
        if dims["hpctoolkit"]:      # TODO: shouldn't require an HPCToolkit if no test wants profiling
            
            # run all the tests
            study = Study(studyPath if studyPath else common.workpath)
            if not wantBatch:
                wantBatch = Executor.defaultToBackground()
            Iterate.doForAll(dims, numrepeats, study, wantBatch)
            print
            
            # report results
            if not common.args["build"]:
                reporter = Report()
                reporter.printReport(study, reportspec, sortKeys if len(sortKeys) else argDimSpecs.keys())
            else:
                print
                print "building complete."
        else:
            errormsg("no --hpctoolkit paths given and no default hpctoolkit is set")
         
        
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
            


    def clean(self, studies, tests, dependencies):
        
        from os        import listdir
        from os.path   import join
        import spackle        
        import common
        from common    import options, yesno, verbosemsg, debugmsg, workpath
        from study     import Study                                      

        def confirm(what):
            ask    = "Really delete all {}?".format(what)
            cancel = "Ok, will not delete them."
            return ("force" in options) or yesno(ask, cancel)
            
        # delete studies if desired
        if studies and confirm("study directories"):
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


    def selftest(self, testspec="all", reportspec="", studyPath=None):
        
        import common
        from dimension import TestDim, ConfigDim, HPCTkitDim, ProfileDim
        from study     import Study
        from iterate   import Iterate
        from report    import Report
        from executor  import Executor
                
#       # run tests, reporting results as we go
        dims  = {"tests":      TestDim(testspec, selftest=True),
                 "build":      ConfigDim.defaultDim(),
                 "hpctoolkit": HPCTkitDim.defaultDim(),
                 "profile":    ProfileDim.defaultDim()
                }
        study = Study(studyPath if studyPath else common.workpath)
        Iterate.doForAll(dims, 1, study, Executor.defaultToBackground())
        print
            
        # report results
        reporter = Report()
        reporter.printReport(study, reportspec, [])
    

    #----------------------------#
    # Instance methods - private #
    #----------------------------#

    # support for deferred execution
    def _runOne(self, encodedArgs):
        
        from run import Run
        from common import debugmsg
        
        debugmsg("_runOne {}".format(encodedArgs))
        runArgs = Run.decodeInitArgs(encodedArgs) + (False, )  # + wantBatch
        debugmsg("_runOne runArgs = {}".format(runArgs))
        runOb   = Run(*runArgs)
        runOb.run(echoStdout=False)
        debugmsg("_runOne done")

        
    def _miniapps(self):
         
        from os.path import join
        import spack
        from spack.repo import Repo
        from common import own_spack_home
             
        # iterate over builtin packages
        builtin = Repo(join(own_spack_home, "var", "spack", "repos", "builtin"))
        for name in builtin.packages_with_tags("proxy-app"):
            p = builtin.get(name)
            url = p.url if hasattr(p, "url") and p.url else "None"
            print "name: "+p.name, "\n", "  homepage: "+p.homepage, "\n", "  url: "+url, "\n"
    
    
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
            if test.builtin(): return
            
            # check if repo has an up-to-date package for the test
            name = test.name()
            packagePath = join(repopath, "packages", name)
            if exists(packagePath):
                needPackage = test.hasChanged()
            else:
                needPackage = True
                
            # if not, update package
            if needPackage:
                HPCTest._addPackageForTest(test)
                test.markUnchanged()
                
        Test.forEachDo(ensureOneTest)
    
    
    @classmethod
    def _addPackageForTest(cls, test):
        
        from os import mkdir
        from os.path import exists, join
        from shutil import copy, rmtree
        import spackle
        from common import debugmsg, repopath
        
        testName = test.name()
        testPath = test.path()
        
        debugmsg("adding package for test {}".format(testPath))
        packagePath = join(repopath, "packages", testName)
    
        # remove installed versions of package if any
        if exists(packagePath):
            cmd = "uninstall --all --force --yes-to-all {}".format(testName)
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


from os.path import isfile
from shutil import copyfile
from common import infomsg, errormsg


# (1) establish preconditions for initializing the config system...

# homepath is needed for everything else
common.homepath = normpath( join(dirname(realpath(__file__)), "..", "..") )
environ["HPCTEST_HOME"] = common.homepath

# paths needed to initialize Spack's location
_internalpath   = join(common.homepath, "internal")
common.own_spack_home = join(_internalpath, "spack")
common.own_spack_module_dir = join( common.own_spack_home, "lib", "spack" )

# sys.path adjustment is needed to load Spack modules
sys.path[1:0] = [ common.own_spack_module_dir,
                  join(common.own_spack_module_dir, "external"),
                  join(common.own_spack_module_dir, "external", "yaml", "lib"),
                  join(common.own_spack_module_dir, "llnl"),
                ]

# set up our private Spack installation if not already present
if not isdir(common.own_spack_home):
    
    # inits to set up our own Spack, done only the first time HPCTest runs
    
    infomsg("Setting up internal Spack...")
    
    spack_version   = "0.12.1"
    spack_tarball   = join(_internalpath, "spack-{}.tar.gz".format(spack_version))
    spack_extracted = join(_internalpath, "spack-{}".format(spack_version))
    spack_dest      = join(_internalpath, "spack")
    system("cd {}; tar xzf {}".format(_internalpath, spack_tarball))
    rename(spack_extracted, spack_dest)

    infomsg("Spack found these compilers automatically:")
    spackle.do("compilers")
    infomsg("To add more existing compilers or build new ones, use 'hpctest spack <spack-cmd>' and")
    infomsg("see 'Getting Started > Compiler configuration' at spack.readthedocs.io.\n")

# Spack is needed to read yaml files in initConfig
spackle.initSpack()

# (2) now we can set up configuration system so configs can specify important paths
configpath = join(common.homepath, "config.yaml")
if not isfile(configpath):
    defaultpath = join(_internalpath, "src", "config-data", "config-default.yaml")
    try:
        copyfile(defaultpath, configpath)
    except Exception as e:
        errormsg("config.yaml is missing and can't be created with defaults: {}".format(str(e)))
configuration.initConfig()

# (3) finally we can initialize important user-visible paths, possibly from config settings
_whichHpcrun         = common.whichDir("hpcrun")
_hpctkLocal          = dirname(_whichHpcrun) if _whichHpcrun else None  # 'dirname' to get hpctoolkit install dir from 'bin' dir
common.hpctk_default = configuration.get("profile.hpctoolkit.path", _hpctkLocal)
common.hpctk_default = expanduser(common.hpctk_default) if common.hpctk_default else None
common.testspath     = join(common.homepath, "tests")
common.repopath      = join(_internalpath, "repos", "tests")
common.workpath      = join(common.homepath, "work")
if not isdir(common.workpath): makedirs(common.workpath)

# set up private repo
HPCTest._ensureRepo()

# make our general-purpose hidden directory
hiddenDir = join(common.homepath, ".hpctest")
if not isdir(hiddenDir): makedirs(hiddenDir)







