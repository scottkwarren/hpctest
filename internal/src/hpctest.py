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




class HPCTest():
    
    import common
    import util
    
    global checksumName
    checksumName = ".checksum"
        
    def __init__(self, extspackpath=None, homepath=None):
        
        from os import environ, makedirs, system, rename
        from os.path import dirname, join, normpath, realpath, expanduser, isdir, splitext
        import sys
        import common, configuration, spackle, util
        from common import infomsg, warnmsg, errormsg
        from testspec   import TestSpec
        from configspec import ConfigSpec
        from stringspec   import StringSpec
        from common import whichDir
        global dimensions, dimspecDefaults, dimspecClasses, _testDirChecksum
    
        # determine important paths
        common.homepath  = normpath( homepath if homepath else join(dirname(realpath(__file__)), "..", "..") )
        internalpath = join(common.homepath, "internal")
        common.ext_spack_home = extspackpath  # ok to be None
        common.own_spack_home = join(internalpath, "spack")
        common.own_spack_module_dir = join( common.own_spack_home, "lib", "spack" )
        common.testspath = join(common.homepath, "tests")
        common.repopath  = join(internalpath, "repos", "tests")
        common.workpath  = join(common.homepath, "work")
        if not isdir(common.workpath): makedirs(common.workpath)

        # set up local spack if necessary
        if not isdir(common.own_spack_home):
            
            infomsg("Setting up internal Spack...")
            
            spack_version   = "0.11.2"
            spack_tarball   = join(internalpath, "spack-{}.tar.gz".format(spack_version))
            spack_extracted = join(internalpath, "spack-{}".format(spack_version))
            spack_dest      = join(internalpath, "spack")
            system("cd {}; tar xzf {}".format(internalpath, spack_tarball))
            rename(spack_extracted, spack_dest)
            
            infomsg("Spack found these compilers automatically:")
            spackle.do("compilers")
            infomsg("To add more existing compilers or build new ones, use 'hpctest spack <spack-cmd>' and")
            infomsg("see 'Getting Started / Compiler configuration' at spack.readthedocs.io.\n")

        # adjust environment accordingly
        environ["HPCTEST_HOME"] = common.homepath
        sys.path[1:0] = [ common.own_spack_module_dir,
                          join(common.own_spack_module_dir, "external"),
                          join(common.own_spack_module_dir, "external", "yaml", "lib"),
                          join(common.own_spack_module_dir, "llnl"),
                        ]

        # set up configuration system
        configuration.initConfig()    # must come after paths, spack,and environ are initialized

        # set up private repo
        self._ensureRepo()
        
        # get install dir of hpctoolkit on $PATH, if any
        hpctkFromPATH = whichDir("hpcrun")
        hpctkFromPATH = dirname(hpctkFromPATH) if hpctkFromPATH else None  # 'dirname' to get hpctoolkit install dir from 'bin' dir
        hpctkDefault  = configuration.get("profile.hpctoolkit path", hpctkFromPATH)
        hpctkDefault  = expanduser(hpctkDefault) if hpctkDefault else None

        msgfunc = warnmsg if common.subcommand == "init" else errormsg if common.subcommand == "run" else None
        if (not hpctkDefault) and msgfunc:
            msgfunc("no default HPCToolkit specified for profiling.\n"
                    "\n"
                    "To run profiling tests, specify '--hpctookit <path to bin dir>' on each 'hpctest run' command line.\n"
                    "To avoid specifying '--hpctoolkit' every time, do one of the following:\n"
                    "- edit hpctest/config.py to specify a default HPCToolkit path\n"
                    "- ensure that an HPCToolkit instance is on your $PATH to serve as default.\n"
                    "\n"
                    )
        
        # dimension info (requires paths and config to be set up)
        dimensions      = set(("tests", "build", "hpctoolkit", "profile"))
        dimspecClasses  = { "tests":TestSpec,    "build":ConfigSpec, "hpctoolkit":StringSpec, "profile":StringSpec }
        dimspecDefaults = { "tests":             "all",    
                            "build":             "%" + configuration.get("build.compiler", "gcc"),     
                            "hpctoolkit":        hpctkDefault,
                            "profile":           configuration.get("profile.hpctoolkit.hpcrun params",    "-e REALTIME@10000") + ";" +
                                                 configuration.get("profile.hpctoolkit.hpcstruct params", "")                  + ";" +
                                                 configuration.get("profile.hpctoolkit.hpcprof params",   "")
                          }
    
    
    def init(self):
    
        # all the necessary work is done in __init__, so nothing here
        pass

        
    def run(self, dimStrings={}, args={}, numrepeats=1, reportspec="", sortKeys=[], workpath=None):
        
        import common
        from common     import debugmsg, options, errormsg
        from testspec   import TestSpec
        from configspec import ConfigSpec
        from study      import Study
        from iterate    import Iterate
        from report     import Report
        global dimensions, dimspecDefaults, dimspecClasses
                
        # decode the odict of dimension strings into a complete odict of dimension specs, with default specs for missing dimensions
        dims = {}
        for dimName in dimensions:
            if dimName in dimStrings:
                str = dimStrings[dimName]
            else:
                str = dimspecDefaults[dimName]
            dims[dimName] = dimspecClasses[dimName](str) if str else None
            
        # check preconditions and run tests if ok
        if dims["hpctoolkit"]:   # TODO: shouldn't require an HPCToolkit if no test wants profiling
            
            # run all the tests
            study = Study(workpath if workpath else common.workpath)
            nonempty = Iterate.doForAll(dims, args, numrepeats, study)
            print "\n"
            
            # report results
            if nonempty:
                reporter = Report()
                reporter.printReport(study, reportspec, sortKeys if len(sortKeys) else dimStrings.keys())
                
        else:
            errormsg("no HPCToolkit specified for profiling.\n"
                     "To fix this do one of the following:\n"
                     "- use '--hpctookit <path-to-bin-dir>' on command line\n"
                     "- edit hpctest/config.py to specify a default path\n"
                     "- ensure that an HPCToolkit instance is on your $PATH.\n"
                     "\n"
                    )
         
        
    def report(self, studypath, reportspec="", sortKeys=[]):
        
        from os         import listdir
        from os.path    import join, isdir
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
        from os.path   import join, isdir
        import spack
        import spackle        
        import common
        from common    import options, yesno, infomsg, verbosemsg, debugmsg
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

        
#     def miniapps(self):
#         
#         from os.path import join
#         import spack
#         from spack.repository import Repo
#         from common import own_spack_home
#         
#         # iterate over builtin packages
#         builtin = Repo(join(own_spack_home, "var", "spack", "repos", "builtin"))
#         for name in builtin.packages_with_tags("proxy-app"):
#             p = builtin.get(name)
#             print "name: " + p.name, "\n", "  homepage: " + p.homepage, "\n", "  url: " + (p.url if p.url else "None"), "\n"

    
    def _ensureRepo(self):

        import os, spack
        import common
        
        # customize settings of builtin repo
        spack.config.update_config("config", {"verify_ssl": False}, scope="site")  # some builtin packages we want to use have wrong checksums
        spack.insecure = True

        # create new private repo for building test cases
        noRepo = spack.repo.get_repo("tests", default=None) is None
        if noRepo: self._makeInternalRepo("tests")
        self._ensureTests()
        if noRepo:
            self._addInternalRepo(common.repopath)
        else:
            self._internalRepoChanged(common.repopath)

        # extend external repo if one was specified
        pass


    def _makeInternalRepo(self, dirname):
        
        from os.path import join, isdir
        from shutil import rmtree
        import spack
        from spack.repository import create_repo
        from common import homepath

        # this just makes a repo directory -- it must be added to Spack once populated
        repoPath = join(homepath, "internal", "repos", dirname)
        if isdir(repoPath): rmtree(repoPath, ignore_errors=True)
        namespace = dirname
        _ = create_repo(repoPath, namespace)
        
        return repoPath


    def _addInternalRepo(self, repoPath):

        import spack
        from spack.repository import Repo, FastPackageChecker

        # adding while preserving RepoPath representation invariant is messy
        # ...no single operation for this is available in current Spack code
        
        # update Spack's config
        repos = spack.config.get_config('repos', "site")
        if isinstance(repos, list):
            repos.insert(0, repoPath)
        else:
            repos = [ repoPath ]
        spack.config.update_config('repos', repos, "site")
        
        # add to Spack's RepoPath
        repo = Repo(repoPath)
        spack.repo.put_first(repo)


    def _internalRepoChanged(self, repoPath):

        import spack
        from spack.repository import Repo
        from common import assertmsg

        # update Spack's current RepoPath
        assertmsg(len(spack.repo.repos) == 2, "unexpected RepoPath length while updating Spack for changed internal repo")
        spack.repo.repos[0] = Repo(repoPath)


    def _ensureTests(self):

        from os.path import join, exists
        from util.checksumdir import dirhash
        from common import options, homepath, forTestsInDirTree, repopath
        import spack
    
        def ensureTest(testDir, testYaml):
            
            if "nochecksum" in options: return
            if testYaml["config"] == "spack-builtin": return
            name = testYaml["info"]["name"]
            checksumPath = join(testDir, checksumName)
            
            # check if repo has an up-to-date package
            newChecksum = dirhash(testDir, hashfunc='md5', excluded_files=[checksumName])
            packagePath = join(repopath, "packages", name)
            if exists(packagePath):
                # compare old and new checksums
                if exists(checksumPath):
                    with open(checksumPath) as old: oldChecksum = old.read()
                else:
                    oldChecksum = "no checksum yet"
                needPackage = newChecksum != oldChecksum
            else:
                needPackage = True
                
            # update package if test has changed
            if needPackage:
                self._addPackageForTest(testDir, name)
                            
                # save new checksum
                with open(checksumPath, 'w') as new:
                    new.write(newChecksum)
                
        testsDir = join(homepath, "tests")
        forTestsInDirTree( testsDir, lambda(a, b): ensureTest(a, b) )   # 


    def _addPackageForTest(self, testPath, name):
        
        from os import mkdir, devnull
        from os.path import exists, join
        from shutil import copy, rmtree
        import spack
        import spackle
        from common import debugmsg, repopath
        
        debugmsg("adding package for test {}".format(testPath))
        packagePath = join(repopath, "packages", name)

        # remove installed versions of package if any
        if exists(packagePath):
            cmd = "uninstall --all --force --yes-to-all {}".format(name)
            spackle.do(cmd, stdout="/dev/null", stderr="/dev/null")   # installed dependencies are not removed
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
            self._generatePackagePy(hpath, packagePath)


    def _generatePackagePy(self, hpath, ppath):
        
        # hpath => hpctest.yaml file to generate from
        # ppath => package directory to generate into
        
        from common import notimplemented
        notimplemented("hpctest._generatePackagePy")






