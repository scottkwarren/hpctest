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




# DIRTY # PENDING SPACK 0.14.1 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def initSpack():

    from os import system
    from os import rename
    from os.path import isdir, join
    from common import internalpath, own_spack_home, infomsg, fatalmsg
    import spackle
    
    infomsg("Setting up internal Spack...")
    
    # extract our Spack from tar file
    spack_version   = spackle.supported_version()
    spack_tarball   = join(internalpath, "spack-{}.tar.gz".format(spack_version))
    spack_extracted = join(internalpath, "spack-{}".format(spack_version))
    spack_dest      = join(internalpath, "spack")
    system("cd {}; tar xzf {}".format(internalpath, spack_tarball))
    if not isdir(spack_extracted):
        fatalmsg("Internal Spack version {} cannot be extracted.".format(spack_version))
    rename(spack_extracted, spack_dest)
        
    # add our tests repo
    own_repo = join(internalpath, "repos", "tests")
    spackle.do("repo add --scope site {}".format(own_repo))

    # avoid checking repo tarball checksums b/c they are often wrong in Spack's packages
#     spackle.do("config --scope site add config:verify_ssl:False")
#     spackle.do("config --scope site add config:checksum:False")
    from spack.config import set as xset        # PENDING SPACK 0.14.1
    xset("config:verify_ssl", False, "site")    # PENDING SPACK 0.14.1
    xset("config:checksum",   False, "site")    # PENDING SPACK 0.14.1
    
    # display available compilers
    infomsg("Spack found these compilers automatically:")
    spackle.do("compilers")
    infomsg("To add more existing compilers or build new ones, use 'hpctest spack <spack-cmd>' and")
    infomsg("see 'Getting Started > Compiler configuration' at spack.readthedocs.io.\n")


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


# DIRTY <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def parseSpec(specString):
    
    from spack.cmd import parse_specs
    return parse_specs(specString)


# DIRTY <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def isInstalled(spec):
    
    # a list of *installed* packages matching 'spec'
    
    import spack
    return spack.store.db.query(spec, installed=True)


# DIRTY <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def getDependents(spec):
    
    # return list of *installed* packages which depend on the given spec's package(s).
    # in HPCTest, if the returned list is empty then the spec denotes a built test (not a dependency)
    
    import spack
    return spack.store.db.installed_relatives(spec, 'parents', True)


# DIRTY <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def hasDependents(spec):
    
    # return wheether there are any *installed* packages which depend on the given spec's package(s).
    
    import spackle
    return len( spackle.getDependents(spec) ) > 0
    

# DIRTY <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def concretizeSpec(spec):
    
    spec.concretize()       # TODO: check that this succeeds


#------------#
#  Packages  #
#------------#

# DIRTY <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def allPackageNames(namespace):
    
    # for HPCTest, namespace must be "builtin" or "tests"
    # result is a set of strings for all packages in given namespace, installed or not
    
    import spack
    return spack.repo.path.get_repo(namespace).all_package_names()


# DIRTY <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def packageFromSpec(spec):
    
    import spack
    return spack.repo.path.get(spec)


# DIRTY <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def setDIY(package, diyPath):
    
    from spack.stage import DIYStage
    package.stage = DIYStage(diyPath)







    
    