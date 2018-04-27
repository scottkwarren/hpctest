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




# Executing a Spack command

def do(cmdstring):
    
    import os, common
    os.system(common.own_spack_home + "/bin/spack " + cmdstring)    # cmdstring contents must be shell-escaped by caller


def extDo(cmdstring):
    
    import os, common
    os.system(common.ext_spack_home + "/bin/spack " + cmdstring)    # cmdstring contents must be shell-escaped by caller



def execute(cmd, cwd=None, env=None, output=None, error=None):
       
    import os, subprocess
    from spack.util.executable import ProcessError
       
    try:
           
        if cwd:
            oldwd  = os.getcwd()
            os.chdir(cwd)
   
        proc = subprocess.Popen(cmd, shell=True, stdin=None, stdout=output, stderr=error, env=env)
        out, err = proc.communicate()
   
        if proc.returncode != 0:
            raise ProcessError('Exit status %d:' % proc.returncode)
   
    except OSError as e:
        raise ProcessError('%s: %s' % (self.exe[0], e.strerror))
   
    except subprocess.CalledProcessError as e:
        raise ProcessError(str(e), "exit status %d" % proc.returncode)
   
    finally:
        if env: os.chdir(oldwd)
           
    # raises spack.util.executable.ProcessError if execution fails


# Transputting a YAML file

def readYamlFile(path):
    
    import spack, yaml
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
    import spack, yaml
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


def removeRepo(repo):
    
    # spack.repo is a RepoPath. RepoPath.remove is broken:
    # it removes from RepoPath.by_name but NOT from RepoPath.by_namespace.
    # this function does the whole job. Cf. RepoPath.remove and RepoPath._add.
    
    import spack
    from spack.util.naming import NamespaceTrie
    
    spack.repo.repos.remove(repo)
    _ = spack.repo.by_path.pop(repo.root, None)
    
    # removing from .by_namespace is messy b/c NamespaceTrie has no 'remove' method
    # instead, we make a new one and re-add each repo
    spack.repo.by_namespace = NamespaceTrie()
    for r in spack.repo.repos:
        spack.repo.by_namespace[r.full_namespace] = r





    
    