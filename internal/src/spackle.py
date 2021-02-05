################################################################################
#                                                                              #
#  spackle.py                                                                  #
#  thin wrappers around Spack cmd lines to expose operations we need           #
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


#------------------#
#  Initialization  #
#------------------#


def supportedVersion():
    
    return "0.16.0"     # 2020-11-18


# avoid checking repo tarball checksums b/c they are often wrong in Spack's packages
# ???
#     spackle.do("config --scope site add config:verify_ssl:False")
#     spackle.do("config --scope site add config:checksum:False")


def initSpack():

    from os import system, rename
    from os.path import isdir, join
    import common
    from common import internalpath, own_spack_home, repopath, infomsg, fatalmsg
    import spackle
    from hpctest import HPCTest

    # set up our repo
    changedPackages = HPCTest._ensureRepo()

    if not isdir(common.own_spack_home):
        
        infomsg("setting up internal Spack...")
        
        # extract our Spack from tar file
        spack_version   = spackle.supportedVersion()
        spack_tarball   = join(common.internalpath, "spack-{}.tar.gz".format(spack_version))
        spack_extracted = join(common.internalpath, "spack-{}".format(spack_version))
        system("cd {}; tar xzf {}".format(common.internalpath, spack_tarball))
        if not isdir(spack_extracted):
            fatalmsg("Internal Spack version {} cannot be extracted.".format(spack_version))
        rename(spack_extracted, common.own_spack_home)
        
        # display available compilers
        infomsg("Spack found these compilers automatically:")
        spackle.do("compilers", echo=True)
        infomsg("To add more existing compilers or build new ones, use 'hpctest spack <spack-cmd>' and")
        infomsg("see 'Getting Started > Compiler configuration' at spack.readthedocs.io.\n")

        # add our tests repo
        spackle.do("repo add --scope site {}".format(repopath), echo=True)
    
        # avoid checking repo tarball checksums b/c they are often wrong in Spack's packages
    # ???
    #     spackle.do("config --scope site add config:verify_ssl:False")
    #     spackle.do("config --scope site add config:checksum:False")
    # ???
    #     from spack.config import set as xset        # PENDING SPACK 0.14.1
    #     xset("config:verify_ssl", False, "site")    # PENDING SPACK 0.14.1
    #     xset("config:checksum",   False, "site")    # PENDING SPACK 0.14.1
    # ???
    #     import spack
    #     from spack import config                        # PENDING SPACK 0.14.1
    #     config.set("config:verify_ssl", False, "site")  # PENDING SPACK 0.14.1
    #     config.set("config:checksum",   False, "site")  # PENDING SPACK 0.14.1
        
    else:
        # remove out of date built package binaries
        for name in changedPackages:
            spackle.uninstall(name)
    

#------------#
#  Commands  #
#------------#

def do(cmdstring, echo=False, stdout="/dev/stdout", stderr="/dev/stderr"):

    # cmdstring contents must be shell-escaped by caller, including the 'stdout' & 'stderr' args
        
    import os, subprocess, common
    from tempfile import mktemp
    
    out = stdout if echo else mktemp()
    err = stderr if echo else mktemp()

    with open(out, "a") as outf, open(err, "a") as errf:
        shellcmd = common.own_spack_home + "/bin/spack " + cmdstring
        env = os.environ.copy()
        env.update(PYTHONPATH = "")   # PYTHONPATH breaks python in subprocess if set
        status = subprocess.call(shellcmd, shell=True, env=env, stdout=outf, stderr=errf)
        
    if echo:
        outstr = ""
        errstr = ""
    else:
        with open(out, "r") as outf, open(err, "r") as errf:
            outstr = outf.read()
            errstr = errf.read()

    return outstr, errstr


def uninstall(name):
    
    import spackle
    
    cmd = "uninstall --all --force --yes-to-all {}".format(name)
    spackle.do(cmd)


#---------#
#  Specs  #
#---------#

def isSpecInstalled(spec):

    import spackle
    from common import BadBuildSpec

    spackCmd = "find {0}".format(spec)
    out, err = spackle.do(spackCmd)
    
    if "Error" in err:  # could just be warnings
        lines = err.split("\n")
        msg = lines[0]
        msg = msg.replace("==> Error: ", "")
        msg = msg.strip().strip(":")
        msg = msg + " ('{}')".format(spec)
        raise BadBuildSpec(msg)
    
    return "No package matches the query" not in out


def installSpec(spec, srcDir = None):

    import spackle
    from common import BuildFailed

    spackle.do("clean")    # removes all leftover build stage directories

    if srcDir:
        spackCmd = "dev-build -d {1} {0}".format(spec, srcDir)
    else:
        spackCmd = "install --keep-stage --dirty {0}".format(spec)

    out, err = spackle.do(spackCmd)
    if "Error" in err:  # could just be warnings
        lines = err.split("\n")
        try:
            msg = next(s for s in lines if "errors found" in s)
        except:
            msg = lines[0]
        msg = msg.strip().strip(":")
        raise BuildFailed(msg)
####    raise Exception(err.replace("==> Error: ", ""))    # for Spack 0.12.0


def specConcretized(spec):
    
    import spackle

    spackCmd = "spec {0}".format(spec)
    out, err = spackle.do(spackCmd)
    ok = len(err) == 0

    if ok:
        lines = out.split("\n")
        concrete = lines[6]
    else:
        concrete = spec  ## ???
        
    return concrete


def specPrefix(spec):
    
    import spackle

##  spec = specConcretized(spec)        # fixes some bug -- what??
    spackCmd = "location --install-dir '{0}'".format(spec)
    out, err = spackle.do(spackCmd)
    
    ok = len(err) == 0
    return out[:-1] if ok else None


def mpiPrefix(spec):
    
    import spackle
    from util.yaml import readYamlString
    from common import errormsg, ExecuteFailed
    
    # get installed packages & their details
    spackCmd = "spec -y {0}".format(spec)
    out, err = spackle.do(spackCmd)
    if err and "Warning:" not in err:
        msg = "invalid spec {}: {}".format(spec, err)
        errormsg(msg)
        raise ExecuteFailed(msg)
    else:
        outDict, _ = readYamlString(out)
        packageDicts = outDict["spec"]      # list of dicts each with a single key, a package name    
                                            # key's value is a dict of details
    
        # find mpi provider and its details
        providers = spackle.mpiProviders()
        mpiDicts  = [d for d in packageDicts if d.keys()[0] in providers]
        mpiDict   = mpiDicts[0]
        
        # make a spec for the mpi provider used in test spec
        # TODO: this only preserves name & compiler; need to make spec from complete yaml dict
        mpiName = mpiDict.keys()[0]
        mpiSpec = ( mpiName
                    + "@" + mpiDict[mpiName]["version"]
                    + "%" + mpiDict[mpiName]["compiler"]["name"]
                            + "@" + mpiDict[mpiName]["compiler"]["version"]
                  )
    
        # get mpi provider's install prefix
        prefix = spackle.specPrefix(mpiSpec)
    
    return prefix


global providers
providers = None
def mpiProviders():
    
    import spackle
    global providers
    
    if not providers:
        out, _    = spackle.do("providers mpi")
        words     = set( {s.strip() for s in out.split()} )
        providers = { w.split("@")[0] for w in words }
        
    return providers


#------------#
#  Packages  #
#------------#

def installedPackageNames(explicit=False, implicit=False):
    
    import spackle
    from common import fatalmsg
    
    flag = "  " if explicit and implicit     else \
           "-x" if explicit and not implicit else \
           "-X" if implicit and not explicit else \
           fatalmsg("spackle.installedPackageNames called incorrectly w/ explicit, implicit both false")
    
    # cmd says to print names of all installed packages
    spackCmd = "find {0}".format(flag)
    out, _ = spackle.do(spackCmd)

    names  = out.split("\n")[2:]
    names  = " ".join( names ).split()  # trick: remove extraneous blank elements due to extra newlines

    return names

        


  