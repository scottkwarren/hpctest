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


#------------------#
#  Initialization  #
#------------------#

def initSpack():

    import spack
    import spack.config     # necessay to force loading the 'config' module,
                            # else 'spack.config' fails below
    
    # avoid checking repo tarball checksums b/c they are often wrong in Spack's packages
    spack.config.config.update_config("config", {"verify_ssl": False}, scope="site")  # some builtin packages we want to use have wrong checksums


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


def extDo(cmdstring):
    
    import os, common
    os.system(common.ext_spack_home + "/bin/spack " + cmdstring)    # cmdstring contents must be shell-escaped by caller


def execute(cmd, cwd=None, env=None, output=None, error=None):
    # raises spack.util.executable.ProcessError if execution fails
       
    import os, subprocess
    from spack.util.executable import ProcessError
       
    try:
           
        if cwd:
            oldwd  = os.getcwd()
            os.chdir(cwd)
   
        process = subprocess.Popen(cmd, shell=True, stdin=None, stdout=output, stderr=error, env=env)
        out, err = process.communicate()
   
        if process.returncode != 0:
            raise ProcessError('Exit status %d:' % process.returncode)
   
    except subprocess.CalledProcessError as e:
        raise ProcessError(str(e), process.returncode)
    except OSError as e:
        raise ProcessError("%s: %s".format(self.exe[0], e.strerror))
    except Exception as e:
        raise ProcessError("unexpected error: " + str(e))
    finally:
        if cwd: os.chdir(oldwd)


#---------#
#  Specs  #
#---------#

def parseSpec(specString):
    
    import spack
    import spack.cmd
    return spack.cmd.parse_specs(specString)


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


def uninstall(name):
    
    import spackle
    
    cmd = "uninstall --all --force --yes-to-all {}".format(name)
    spackle.do(cmd, echo=False)


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


#--------------#
#  YAML files  #
#--------------#

def readYamlFile(path):
    
    import spack
    import ruamel.yaml as yaml
    from common import options, debugmsg

    if "verbose" in options:
        debugmsg("reading yaml file at {}".format(path))
        
    try:
        with open(path, 'r') as f:
            try:
                object, msg = yaml.load(f), None
            except:
                object, msg = None, "file has syntax errors and cannot be used"
    except Exception as e:
        if isinstance(e, OSError) and e.errno == errno.EEXIST:
            object, msg = None, "yaml file to be read is missing"
        else:
            object, msg = None, "yaml file cannot be opened: (error {0}, {1})".format(e.errno, e.strerror)
    
    if "verbose" in options:
        debugmsg("...finished reading yaml file with result object {} and msg {}".format(object, repr(msg)))
    
    return object, msg


def writeYamlFile(path, object):
    
    from collections import OrderedDict     # to make output text file will have fields in order of insertion
    import sys
    import spack
    import ruamel.yaml as yaml
    from common import options, debugmsg, fatalmsg

    def ordered_dump(data, stream=None, Dumper=yaml.Dumper, **kwds):    # adaptor to let PyYAML use OrderedDict
        class OrderedDumper(Dumper):
            pass
        def _dict_representer(dumper, data):
            return dumper.represent_mapping(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, data.items())
        OrderedDumper.add_representer(OrderedDict, _dict_representer)
        return yaml.dump(data, stream, OrderedDumper, **kwds)
        

    if "verbose" in options: debugmsg("writing yaml file at {}".format(path))
    msg = None
    try:
        
        if path:
            with open(path, 'w') as f:
                try:
                    ordered_dump(object, stream=f, Dumper=yaml.SafeDumper, default_flow_style=False)
                except Exception as e:
                    fatalmsg("can't write given object as YAML (error {})\nobject: {}".format(e.message, object))
        else:
            try:
                ordered_dump(object, stream=sys.stdout, Dumper=yaml.SafeDumper, default_flow_style=False)
            except Exception as e:
                fatalmsg("can't write given object as YAML (error {})\nobject: {}".format(e.message, object))
            
    except Exception as e:
        msg = "file cannot be opened for writing: (error {})".format(e)
    if "verbose" in options: debugmsg("...finished writing yaml file with msg {}".format(repr(msg)))





    
    