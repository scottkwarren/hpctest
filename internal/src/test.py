################################################################################
#                                                                              #
#  test.py                                                                     #
#  a test case specified by path to its directory                              #
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




class Test():
    
    _checksumFilename = ".checksum"
    _yamlFilename     = "hpctest.yaml"


    @classmethod
    def isTestDir(cls, path):
        
        from os.path import isfile, join
        return isfile(join(path, Test._yamlFilename))


    @classmethod
    def forEachDo(cls, action):
        
        import os
        from os.path import join
        from common import homepath
        
        testsRoot = join(homepath, "tests")
        for dir, _, _ in os.walk(testsRoot, topdown=False):
            if Test.isTestDir(dir):
                action(Test(dir))

    
    def __init__(self, dir):
        
        from common import fatalmsg
        
        if Test.isTestDir(dir):
            self.dir = dir
            self.yamlDict, self.yamlMsg = self._readYaml()
        else:
            fatalmsg("Test.__init__: dir must be a path to a valid test directory but is not ({})").format(dir)


    def builtin(self):
        
        return self.yamlDict["build"] == "builtin" if "build" in self.yamlDict else False


    def cmd(self):
        
        return self._yaml("run.cmd")
        

    def description(self, config, hpctoolkit, profile, forName=False):
        
        ## TODO: use 'hpctoolkit', eg if not the default one, but need short names for the paths
        
        from dimension import TestDim, ConfigDim, HPCTkitDim, ProfileDim
        
        f = "{}:{}:{}" if forName else "{} : {} : {}"
        t = TestDim.format(self.relpath(), forName)
        c = ConfigDim.format(config,       forName)
        p = ProfileDim.format(profile,     forName)
        
        return f.format(t, c, p)


    def hasChanged(self):
        
        from os.path import join, exists
        from util.checksumdir import dirhash

        # get new checksum
        newChecksum = self._computeChecksum()

        # get old checksum
        checksumPath = join(self.dir, Test._checksumFilename)
        if exists(checksumPath):
            with open(checksumPath) as old:
                oldChecksum = old.read()
        else:
            oldChecksum = None
            
        return newChecksum != oldChecksum


    def installProducts(self):
        
        from common import noneOrMore
        return noneOrMore(self._yaml("build.install")) if isinstance(self._yaml("build"), dict) else []


    def markUnchanged(self):
        
        from os.path import join

        checksumPath = join(self.dir, Test._checksumFilename)
        with open(checksumPath, 'w') as cs:
            cs.write(self._computeChecksum())
    

    def name(self):
            
        return self._yaml("info.name")


    def numRanks(self):
        
        return self._yaml("run.ranks", 1)


    def numThreads(self):
        
        return self._yaml("run.threads", 1)


    def path(self):
            
        return self.dir


    def profile(self):
        return self.yamlDict.get("profile", True)


    def relpath(self):
        
        from os.path import relpath, join
        from common import homepath
        return relpath(self.dir, join(homepath, "tests"))


    def runSubdir(self):
        
        return self._yaml("run.dir", ".")


    def valid(self):
        
        return self.yamlDict is not None;


    def version(self):
        
        return self._yaml("info.version", "1.0")
    
    
    def wantProfile(self):
        
        return bool(self.profile())
    

    def yamlErrorMsg(self):
        
        return self.yamlMsg
    

    #-----------------#
    # Private methods #
    #-----------------#

    def _computeChecksum(self):
        
        from util.checksumdir import dirhash
        return dirhash(self.dir, hashfunc='md5', excluded_files=[Test._checksumFilename])


    def _readYaml(self):
     
        from os.path import join, basename
        from spackle import readYamlFile
             
        # read yaml file
        yaml, msg = readYamlFile(join(self.dir, Test._yamlFilename))
         
        # validate and apply defaults
        if not msg:
            if not yaml.get("info"):
                 yaml["info"] = {}
            if not yaml.get("info").get("name"):
                 yaml["info"]["name"] = basename(self.path())
            if not yaml.get("build"):
                 yaml["build"] = {}
            # TODO...
     
        return yaml, msg

    
    def _yaml(self, keypath=None, default=None):
        
        from common import getValueAtKeypath
        return getValueAtKeypath(self.yamlDict, keypath, default)








