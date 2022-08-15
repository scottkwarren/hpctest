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


#----------------------#
# Spack mesage formats #
#----------------------#

# 00000000001111111111222222222233333333334444444444555555555566666666667
# 01234567890123456789012345678901234567890123456789012345678901234567890
#---
# Error: AMG2006@1.0%gcc@9.3.1 matches multiple packages.
#   Matching packages:
#     i54hgah AMG2006@1.0%gcc@9.3.1 arch=linux-rhel7-broadwell
#     3qzyuj4 AMG2006@1.0%gcc@9.3.1 arch=linux-rhel7-broadwell
#   Use a more specific spec.
#---
# 00000000001111111111222222222233333333334444444444555555555566666666667
# 01234567890123456789012345678901234567890123456789012345678901234567890



#------------------#
#  Initialization  #
#------------------#


def supportedVersion():
    
    return "0.18.1"


def initSpack():

    from os import system, symlink
    from os.path import abspath, exists, isfile, isdir, join, basename
    import common
    from common import args, internalpath, repopath, infomsg, fatalmsg
    import spackle
    from hpctest import HPCTest

    # detect a suitable Spack instance, if any 
    if  args["--spack"]:
        home  = args["--spack"]
        where = "'--spack' {}".format(home)
        _assertSpackDir(home)
    else:
        home  = join(common.internalpath, "spack")
        where = "default directory {}".format(home)
    common.own_spack_home = home
    
    # prepare a Spack instance at 'home'
    if isSpackDir(home):
        # remove out of date built package binaries
        changedPackages = HPCTest._ensureRepo()
        for name in changedPackages:
            spackle.uninstall(name)
    else:
        
        infomsg("setting up internal Spack...")
        
        # find a compressed Spack already in our 'internal' directory
        cmd = None  
        for suffix in "develop", spackle.supportedVersion():
            spackName = "spack-" + suffix
            for extension in "tar.gz", "tgz", "tar", "zip":
                compressed = join(common.internalpath, spackName  + "." + extension)
                if isfile(compressed):
                    cmd = "tar xf" if extension == "tar" else "unzip" if extension == "zip" else "tar xzf"
                    break
            if cmd: break
        if cmd:
            system("cd {}; {} {} > /dev/null".format(common.internalpath, cmd, compressed))
            extracted = join(common.internalpath, spackName)
            if isdir(extracted):
                assertSpackDir(extracted)
                infomsg("using compressed Spack file " + compressed)
            else:
                fatalmsg("compressed Spack cannot be extracted from {}".format(compressed))
        else:
            fatalmsg("no compressed Spack found in {}".format(common.internalpath))

        common.own_spack_home = extracted
        symlink(extracted, join(common.internalpath, "spack"))
        
        # display available compilers
        infomsg("Spack found these compilers automatically:")
        infomsg("")
        spackle.do("compilers", echo=True)
        infomsg("")
        infomsg("To add more existing compilers or build new ones, use 'hpctest spack <spack-cmd>' and")
        infomsg("see 'Getting Started > Compiler configuration' at spack.readthedocs.io.\n")
        infomsg("")

        # add our tests repo
        out, err = spackle.do("repo list", echo=False)
        if not ( basename(repopath) in out ):
            spackle.do("repo add --scope site {}".format(repopath), echo=True)        


def isSpackDir(dir):
    
    from os import access, X_OK
    from os.path import isfile, join
    
    exe = join(dir, "bin", "spack")
    return isfile(exe) and access(exe, X_OK)


def assertSpackDir(dir):
    
    from common import assertmsg
    assertmsg(isSpackDir(dir), "No Spack found at {}".format(dir))


#------------#
#  Commands  #
#------------#

def do(cmdstring, echo=False, stdout="/dev/stdout", stderr="/dev/stderr"):

    # cmdstring contents must be shell-escaped by caller, including the 'stdout' & 'stderr' args
        
    import os, subprocess, common
    from os.path import join
    from common import verboseOption
    from tempfile import mktemp
    
    out = stdout if echo else mktemp()
    err = stderr if echo else mktemp()

    with open(out, "a") as outf, open(err, "a") as errf:
        shellcmd = join(common.own_spack_home, "bin/spack ") + verboseOption() + cmdstring
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
    from common import BadBuildSpec, errormsg
    import re
    
    r = re.compile("([^\.]+\.)*([a-zA-Z0-9_\-]+)(@(.+))")
    s = r.search(spec)
    dotPrefix = s.group(1)
    testName  = s.group(2)
    version   = s.group(3)

    spackCmd = "find {0}".format(testName)      # is it installed?   
    out, err = spackle.do(spackCmd)
    
    # when no such package, 'out' gets eg:
    # ==> No package matches the query: tests.amgmk@1.0%gcc\n
    
    # when erroneous query, 'err' gets eg:
    # ==> Error: module 'spack.pkg.tests.fib-pg' has no attribute 'FibPg'\n
    
    if err:
        installed = False
    elif "No package matches" in out: 
        installed = False
    elif "==> 0 packages" in out:
        installed = False
    else:
        installed = True
    
    return installed


def installSpec(spec, srcDir = None, buildOnly = False):

    import spackle
    from common import options, verboseOption, BuildFailed
    verbose = verboseOption()
    
    spackle.do("clean")    # removes all leftover build stage directories

    before  = "--before install" if buildOnly else ""
    if srcDir:
        spackCmd = \
            "dev-build -d {0} {1} '{2}'" \
                .format(srcDir, before, spec)
    else:
        spackCmd =  \
            "install --reuse --keep-stage --dirty --show-log-on-error {0} {1} '{2}'" \
                .format(verbose, before, spec)

    out, err = spackle.do(spackCmd, echo = verbose)
    
    if "Error" in err:  # could just be warnings
        msg = err
        msg = msg.strip().strip(":")
        msg = msg.replace("==> Error: ", "")
        raise BuildFailed(msg)


def specConcretized(spec):
    
    import spackle
    from common import BuildFailed

    spackCmd = "spec --cover nodes {0}".format(spec)
    out, err = spackle.do(spackCmd)
    ok = len(err) == 0

    if ok:
        lines = out.split("\n")
        concrete = " ".join( " ".join(lines[6:]).split() )
    else:
        msg = "spec {} can't be concretized: {}".format(spec, err)
        raise BuildFailed(msg.replace("==> Error: ", ""))
        
    return concrete


def specPrefix(spec):
    
    import spackle
    from common import warnmsg, fatalmsg, BadBuildSpec

    template = "location --install-dir '{0}'"

    cmd = template.format(spec)
    out, err = spackle.do(cmd)
    
    if "matches multiple packages" in err:
        errLines  = err.split("\n")
        firstSpec = errLines[2][12:]
        firstHash = errLines[2][4:11]

        warnmsg("spec matches more than one installed package; using {}/{}"  \
                .format(firstSpec, firstHash))

        cmd = template.format(firstSpec + "/" + firstHash)
        out, err = spackle.do(cmd)
        
    ok = len(err) == 0
    
    if not ok:
        msg = "can't find spec prefix for spec '{}':\n{}".format(spec, err)
        raise BadBuildSpec(msg)
    
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
        # find mpi provider and its details
        outDict, _ = readYamlString(out)
        packages   = outDict["spec"]["nodes"]      # list of dicts each with a single key, a package name                                                # key's value is a dict of details
        providers  = spackle.mpiProviders()
        mpiDicts   = [d for d in packages
                        if d["name"] in providers]
        mpiDict    = mpiDicts[0]
        
        # make a spec for the mpi provider used in test spec
        # TODO: this only preserves name/compiler/version; do we need to make spec from complete yaml dict
        mpiName = mpiDict["name"]
        mpiSpec = ( mpiName
                    + "@" + mpiDict["version"]
                    + "%" + mpiDict["compiler"]["name"]
                            + "@" + mpiDict["compiler"]["version"]
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







        


  
