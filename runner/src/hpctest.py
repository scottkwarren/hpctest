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
        
        from os import environ
        from os.path import dirname, join, normpath, realpath, expanduser
        import sys
        import common, configuration, spackle, util
        from testspec   import TestSpec
        from configspec import ConfigSpec
        from stringspec   import StringSpec
        from util.which import which
        global dimensions, dimspecDefaults, dimspecClasses, _testDirChecksum
    
        # determine important paths
        common.homepath  = normpath( homepath if homepath else join(dirname(realpath(__file__)), "..", "..") )
        common.ext_spack_home = extspackpath  # ok to be None
        common.own_spack_home = join( common.homepath, "runner", "spack" )
        common.own_spack_module_dir = join( common.own_spack_home, "lib", "spack" )
        common.workpath = join(common.homepath, "work")

        # adjust environment accordingly
        environ["HPCTEST_HOME"] = common.homepath
        sys.path[1:0] = [ common.own_spack_module_dir,
                          join(common.own_spack_module_dir, "external"),
                          join(common.own_spack_module_dir, "external", "yaml", "lib"),
                          join(common.own_spack_module_dir, "llnl"),
                        ]

        # set up hpctest's layered configuration system
        configuration.initConfig()    # must come after common.homepath is initialized

        # dimension info (requires paths and config to be set up)
        dimensions      = set(("tests", "configs", "hpctoolkits", "hpctoolkitparams"))
        dimspecClasses  = { "tests":TestSpec, "configs":ConfigSpec, "hpctoolkits":StringSpec, "hpctoolkitparams":StringSpec }
        dimspecDefaults = { "tests":            "all",    
                            "configs":          "%" + configuration.get("build.compiler", "gcc"),     
                            "hpctoolkits":      expanduser( configuration.get("profile.hpctoolkit bin path", dirname(which("hpcrun"))) ), 
                            "hpctoolkitparams": configuration.get("profile.hpctoolkit.hpcrun params",    "-e REALTIME@10000") + ";" +
                                                configuration.get("profile.hpctoolkit.hpcstruct params", "")                  + ";" +
                                                configuration.get("profile.hpctoolkit.hpcprof params",   "")
                          }
        
        
    def run(self, dimStrings={}, args={}, workpath=None):
        
        import common
        from common     import debugmsg, options
        from testspec   import TestSpec
        from configspec import ConfigSpec
        from workspace  import Workspace
        from iterate    import Iterate
        from report     import Report
        global dimensions, dimspecDefaults, dimspecClasses

        self._ensureRepos()
        if not workpath: workpath = common.workpath
                
        # decode the odict of dimension strings into a complete odict of dimension specs, with default specs for missing dimensions
        dims = {}
        for dimName in dimensions:
            if dimName in dimStrings:
                str = dimStrings[dimName]
            else:
                str = dimspecDefaults[dimName]
            dims[dimName] = dimspecClasses[dimName](str)
        
        workspace = Workspace(workpath)
        
        status  = Iterate.doForAll(dims, args, workspace)
        print "\n"
        Report.printReport(workspace)
        print "\n"
        
        return status
        
        
    def report(self, workpath=None):
        
        import common
        from common     import debugmsg, options
        from report     import Report

        if not workpath: workpath = common.workpath ## <<<<<<<<<<<<<<<<<<<<<<< FIX <<<<<<<<<<<<<<<<<<<<<<
                
        print "\n"
        Report.printReport(workspace)
        print "\n"


    def clean(self, workpath=None):
        
        from os        import listdir
        from os.path   import join, isdir
        import common
        from common    import debugmsg
        from workspace import Workspace
        
        if not workpath: workpath = common.workpath
        debugmsg("cleaning work directory {}".format(workpath))
        
        for name in listdir(workpath):
            path = join(workpath, name)
            if isdir(path) and name.startswith("workspace-"):
                Workspace(path).clean()


    def reset(self):
        
        from os import remove
        from os.path import exists, join
        from shutil import rmtree
        from common import homepath, own_spack_home, errormsg
        import spackle

        self.clean()
        
        # remove private repo directories
        tpath = join(homepath, "runner", "repos", "tests")
        if exists(tpath): rmtree(tpath)
        bpath = join(homepath, "runner", "repos", "build")
        if exists(bpath): rmtree(bpath)

        # remove repo paths from Spack's repos.yaml
        with open(join(own_spack_home, "etc", "spack", "repos.yaml"), "w") as f:
            f.write("repos:\n")
        
        # remove checksum file from tests directory
        cpath = join(homepath, "tests", checksumName)
        if exists(cpath): remove(cpath)
        
        # remove all installed packages and leftover build byproducts
        try:
            spackle.do("clean --all")
            rmtree(join(own_spack_home, "opt"))
            spackle.do("reindex")
#           spackle.do("module refresh")    # CONTRARY TO DOCS, 'constraint' arg is mandatory    # could add a package's spec to limit the refresh
        except Exception as e:
            errormsg( "error removing installed packages and their build byproducts ({})".format(str(e)) )

        
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

    
    def _ensureRepos(self):
        # set up our private spack & make it extend the external one if any

        from os.path import join, exists
        from util.checksumdir import dirhash
        from common import options, homepath, infomsg, debugmsg
        global _testDirChecksum
        
        testsDir = join(homepath, "tests")
        checksumPath = join(testsDir, checksumName)
        
        if exists(checksumPath) and "nochecksum" in options:     # 'nochecksum' notwithstanding, need to set up repos if checksum file is missing (ie first run)
            infomsg("skipping check for changes in 'tests' directory because '--nochecksum' option given")
            return
        
        # get old and new checksums
        if exists(checksumPath):
            with open(checksumPath) as old: oldChecksum = old.read()
        else:
            oldChecksum = "no checksum yet"
        newChecksum = dirhash(testsDir, hashfunc='md5', excluded_files=[checksumName])
        
        # check if tests have changed
        if newChecksum != oldChecksum:

            # set up repos anew
            debugmsg("recreating test packages since 'tests' directory has changed")
            debugmsg("... old = {}, new = {}".format(oldChecksum, newChecksum))
            self._setUpRepos()
                        
            # save new checksum -- must follow '_setUpRepos' b/c it deletes this checksum file
            with open(checksumPath, 'w') as new:
                new.write(newChecksum)


    def _setUpRepos(self):

        import sys
        import os
        from os.path import join, isfile
        from common import homepath, readYamlforTest, errormsg
        
        # must start with a clean slate to avoid Spack errrors
        self.reset()
        
        # create new private repo for building test cases
        repoPath = self._makePrivateRepo("tests")
        
        # populate test repo with a package for each test case
        testsPath = join(homepath, "tests")
        for root, dirs, files in os.walk(testsPath, topdown=False):
            
            if isfile(join(root, "hpctest.yaml")):
                yaml, msg = readYamlforTest(root)
                if yaml:  # found a test-case directory
                    if yaml["config"] != "spack-builtin":
                        self._addPackageForTest(repoPath, root, yaml["info"]["name"])
                    else:
                        # existing Spack builtin package will be used for this test
                        pass
                else:
                    errormsg("unusable 'hpctest.yaml' file in test {}: {}".format(root, e.message))
                    
        # add test repo to private Spack
        self._addPrivateRepo(repoPath)

        # extend external repo if one was specified
        pass

# ---------------------------------------------------------------
#                 if yaml["config"] != "spack-builtin":
#                     self._addPackageForTest(repoPath, root, yaml["info"]["name"])
#                 else:
#                     # existing Spack builtin package will be used for this test
#                     pass
# ---------------------------------------------------------------


    def _makePrivateRepo(self, dirname):
        
        from argparse import Namespace
        from os.path import join
        from shutil import rmtree
        import spack
        from spack.cmd.repo import repo_remove
        from spack.repository import create_repo
        from common import homepath

        repoPath = join(homepath, "runner", "repos", dirname)
        namespace = dirname

        # repo must not exist or already be added to Spack
        repos = spack.config.get_config('repos', "site")
        if repoPath in repos:
            repo_remove(Namespace(path_or_namespace=repoPath, scope="site"))
            rmtree(repoPath)

        # this just makes & prepares reoo directory, must be added to Spack once populated
        _ = create_repo(repoPath, namespace)
        
        return repoPath


    def _addPrivateRepo(self, repoPath):

        import spack
        from spack.repository import Repo, FastPackageChecker

        # adding while preserving RepoPath representation invariant is messy
        # ...no single operation for this is available in current Spack code
        repos = spack.config.get_config('repos', "site")
        repos.insert(0, repoPath)
        spack.config.update_config('repos', repos, "site")
        repo = Repo(repoPath)
        spack.repo.put_first(repo)


    def _addPackageForTest(self, repoPath, testPath, name):
        
        from os import mkdir
        from os.path import exists, join
        from shutil import copy
        from common import debugmsg
        
        debugmsg("adding package for test {}".format(testPath))

        # make package directory for this test
        packagePath = join(repoPath, "packages", name)
        mkdir(packagePath)
        
        # copy or generate test's description files
        hpath = join(testPath, "hpctest.yaml")
        ppath = join(testPath, "package.py")
        copy(hpath, packagePath)
        if exists(ppath):
            copy(ppath, packagePath)
        else:
            self._generatePackagePy(hpath, packagePath)
            
        # TODO?? add package to repo


    def _generatePackagePy(self, hpath, ppath):
        
        # hpath => hpctest.yaml file to generate from
        # ppath => package directory to generate into
        notimplemented("hpctest._generatePackagePy")






