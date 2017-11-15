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
    
    def __init__(self, extspackpath=None, homepath=None):
        
        from os import environ
        from os.path import dirname, join, normpath, realpath
        import sys
        import common, spackle
        global _testDirChecksum

        # determine important paths
        common.homepath  = homepath if homepath else normpath( join(dirname(realpath(__file__)), "..", "..") )
        common.ext_spack_home = extspackpath  # ok to be None
        common.own_spack_home = join( common.homepath, "runner", "spack" )
        common.own_spack_module_dir = join( common.own_spack_home, "lib", "spack" )
        
        # adjust environment accordingly
        environ["HPCTEST_HOME"] = common.homepath
        sys.path[1:0] = [ common.own_spack_module_dir,
                          join(common.own_spack_module_dir, "external"),
                          join(common.own_spack_module_dir, "external", "yaml", "lib")
                        ]
        

    def run(self, testSpec, configSpec, workpath):
        
        from common     import debugmsg, options
        from testspec   import TestSpec
        from configspec import ConfigSpec
        from workspace  import Workspace
        from iterate    import Iterate
        from report     import Report

        debugmsg("will run tests {} on configs {} in {} with options {}"
                    .format(testSpec, configSpec, workpath, options))
                
        tests     = TestSpec(testSpec)
        configs   = ConfigSpec(configSpec)
        workspace = Workspace(workpath)
        
        self._ensureRepos()
        status  = Iterate.doForAll(tests, configs, workspace)
        Report.printReport(workspace)
        
        return status


    def clean(self, workpath):
        
        from os        import listdir
        from os.path   import join, isdir
        from shutil    import rmtree
        from common    import debugmsg
        from workspace import Workspace
        
        debugmsg("cleaning work directory {}".format(workpath))
        
        for name in listdir(workpath):
            path = join(workpath, name)
            if isdir(path) and name.startswith("workspace-"):
                Workspace(path).clean()


    def reset(self):
        
        from os import remove
        from os.path import exists, join
        from shutil import rmtree
        from common import homepath, own_spack_home

        # remove private repo directories
        tpath = join(homepath, "runner", "repos", "tests")
        if exists(tpath): rmtree(tpath)
        bpath = join(homepath, "runner", "repos", "build")
        if exists(bpath): rmtree(bpath)
        
        # remove repo paths from Spack's repos.yaml
        with open(join(own_spack_home, "etc", "spack", "repos.yaml"), "w") as f:
            f.write("repos:\n")
        
        # remove checksum file from tests directory
        cpath = join(homepath, "tests", ".checksum")
        if exists(cpath): remove(cpath)
    

    def _ensureRepos(self):
        # set up our private spack & make it extend the external one if any

        from os.path import join, exists
        from util.checksumdir import dirhash
        from common import homepath
        global _testDirChecksum
        
        testsDir = join(homepath, "tests")
        checksumName = ".checksum"
        checksumPath = join(testsDir, checksumName)
        
        # get old checksum
        if exists(checksumPath):
            with open(checksumPath) as old: oldChecksum = old.read()
        else:
            oldChecksum = "no checksum yet"
        
        # compute new checksum
        newChecksum = dirhash(testsDir, hashfunc='md5', excluded_files=[checksumName])
        
        # save new checksum
        with open(checksumPath, 'w') as new: new.write(newChecksum)

        if newChecksum != oldChecksum: self._setUpRepos()


    def _setUpRepos(self):

        import os
        from os.path import join
        from common import homepath

        # create new private repo for building test cases
        repoPath = self._newPrivateRepo("tests")
        
        # populate test repo with a package for each test case
        testsPath = join(homepath, "tests")
        for root, dirs, files in os.walk(testsPath, topdown=False):
            if "hpctest.yaml" in files:  # found a test-case directory
                self._addPackageForTest(repoPath, root)
    
        # create private repo for building test case dependencies
        _ = self._newPrivateRepo("build")
       
        # extend external repo
        pass


    def _newPrivateRepo(self, dirname):
        
        from os.path import join
        from argparse import Namespace
        import spack
        from spack.repository import create_repo
        from spack.cmd.repo import repo_add, repo_remove
        from common import homepath

        repoPath = join(homepath, "runner", "repos", dirname)
        namespace = "hpctest.{}".format(dirname)
        
        repos = spack.config.get_config('repos', "site")
        if repoPath in repos:
            repo_remove(Namespace(path_or_namespace=repoPath, scope="site"))
            
        _ = create_repo(repoPath, namespace)
        repo_add(Namespace(path=repoPath, scope="site"))
        
        return repoPath


    def _addPackageForTest(self, repoPath, testPath):
        
        from os import mkdir
        from os.path import basename, exists, join
        from shutil import copy
        from common import debugmsg
        
        debugmsg("adding package for test {}".format(testPath))

        # make package directory for this test
        name = basename(testPath)
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


    def _generatePackagePy(self, hpath, ppath):
        
        # hpath => hpctest.yaml file to generate from
        # ppath => package directory to generate into
        pass
        









