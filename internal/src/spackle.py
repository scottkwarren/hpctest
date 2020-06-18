################################################################################
#                                                                              #
#  spackle.py                                                                  #
#  thin wrapper around private Spack to expose operations we need              #
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


import sys


###############################
## NONINVASIVE USES OF SPACK ##
###############################


#------------------#
#  Initialization  #
#------------------#

def supported_version():
    
    return "0.12.1"


def initSpack():

    import spack
    import spack.config     # necessay to force loading the 'config' module,
                            # else 'spack.config' fails below
    
    # avoid checking repo tarball checksums b/c they are often wrong in Spack's packages
    spack.config.config.update_config("config", {"verify_ssl": False}, scope="command_line")  # some builtin packages we want to use have wrong checksums
    spack.config.set('config:checksum', False, scope='command_line')


#------------#
#  Commands  #
#------------#

def do(cmdstring, echo=True):

    # cmdstring contents must be shell-escaped by caller, including the 'stdout' & 'stderr' args
        
    import os, common
    
    if echo:
        out = "/dev/stdout"
        err = "/dev/stderr"
    else:
        out = "/dev/null"
        err = "/dev/null"
    os.system(common.own_spack_home + "/bin/spack " + cmdstring + " > {} 2> {}".format(out, err))


def uninstall(name):
    
    import spackle
    
    cmd = "uninstall --all --force --yes-to-all {}".format(name)
    spackle.do(cmd, echo=False)


#---------#
#  Specs  #
#---------#

def parseSpec(specString):
    
    from spack.cmd import parse_specs
    return parse_specs(specString)


def isInstalled(spec):
    
    # a list of *installed* packages matching 'spec'
    
    import spack
    return spack.store.db.query(spec, installed=True)


def getDependents(spec):
    
    # return list of *installed* packages which depend on the given spec's package(s).
    # in HPCTest, if the returned list is empty then the spec denotes a built test (not a dependency)
    
    import spack
    return spack.store.db.installed_relatives(spec, 'parents', True)


def hasDependents(spec):
    
    # return wheether there are any *installed* packages which depend on the given spec's package(s).
    
    import spackle
    return len( spackle.getDependents(spec) ) > 0
    

def concretizeSpec(spec):
    
    spec.concretize()       # TODO: check that this succeeds


#------------#
#  Packages  #
#------------#

def allPackageNames(namespace):
    
    # for HPCTest, namespace must be "builtin" or "tests"
    # result is a set of strings for all packages in given namespace, installed or not
    
    import spack
    return spack.repo.path.get_repo(namespace).all_package_names()


def packageFromSpec(spec):
    
    import spack
    return spack.repo.path.get(spec)


def setDIY(package, diyPath):
    
    from spack.stage import DIYStage
    package.stage = DIYStage(diyPath)


#----------------#
#  Repositories  #
#----------------#

def getRepo(name):
    
    import spack
    return spack.repo.path.get_repo(name, default=None)
    
    
def createRepo(dirname):

    from os.path import join, isdir
    from shutil import rmtree
    import spack
    from spack.repo import create_repo
    from common import homepath

    # this just makes a repo directory -- it must be added to Spack once populated
    repoPath = join(homepath, "internal", "repos", dirname)
    if isdir(repoPath): rmtree(repoPath, ignore_errors=True)
    namespace = dirname
    _ = create_repo(repoPath, namespace)


def updateRepoPath(repoPath):

    import spack
    from spack.repo import Repo
    from common import assertmsg

    # update Spack's current RepoPath
    assertmsg(len(spack.repo.path.repos) == 2, "unexpected RepoPath length while updating Spack for changed internal repo")
    spack.repo.path.repos[0] = Repo(repoPath)


def addRepo(repoPath):

    import spack
    from spack.repo import Repo

    # We need to add a repo *while Spack is running*, which existing Spack code never does.
    # Adding while preserving RepoPath representation invariant is messy
    # ...no single operation for this is available in current Spack code
    
    # update Spack's config
    repos = spack.config.config.get_config('repos', "site")
    if isinstance(repos, list):
        repos.insert(0, repoPath)
    else:
        repos = [ repoPath ]
    spack.config.config.update_config('repos', repos, "site")
    
    # add to Spack's RepoPath
    repo = Repo(repoPath)
    spack.repo.path.put_first(repo)







    
    