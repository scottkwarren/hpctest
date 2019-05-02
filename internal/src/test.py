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
    
    _checksumName = ".checksum"
    _yamlName     = "hpctest.yaml"
    
    
    #---------------#
    # Class methods #
    #---------------#
    
    @classmethod
    def isTestDir(cls, path):
        
        from os.path import isfile, join
        return isfile(join(path, Test._yamlName))


    @classmethod
    def markUnchanged(cls, testDir):
        
        from os.path import join

        checksumPath = join(testDir, Test._checksumName)
        with open(checksumPath, 'w') as cs:
            cs.write(Test._computeChecksum(testDir))


    @classmethod
    def hasChanged(cls, testDir):
        
        from os.path import join, exists
        from util.checksumdir import dirhash

        # get new checksum
        newChecksum = Test._computeChecksum(testDir)

        # get old checksum
        checksumPath = join(testDir, Test._checksumName)
        if exists(checksumPath):
            with open(checksumPath) as old:
                oldChecksum = old.read()
        else:
            oldChecksum = ""
            
        return newChecksum != oldChecksum


    @classmethod
    def forEachDo(cls, action):
        
        import os
        from os.path import join
        from common import homepath
        
        testsRoot = join(homepath, "tests")
        for root, _, _ in os.walk(testsRoot, topdown=False):
            if Test.isTestDir(root):
                yaml, _ = Test._readYaml(root)
                if yaml:
                    found = (root, yaml)
                    action(found)


    @classmethod
    def _computeChecksum(cls, testDir):
        
        from util.checksumdir import dirhash
        return dirhash(testDir, hashfunc='md5', excluded_files=[Test._checksumName])


    @classmethod
    def _readYaml(cls, testDir):
     
        from os.path import join, basename
        from spackle import readYamlFile
             
        # read yaml file
        yaml, msg = readYamlFile(join(testDir, Test._yamlName))
         
        # validate and apply defaults
        if not msg:
            if not yaml.get("info"):
                 yaml["info"] = {}
            if not yaml.get("info").get("name"):
                 yaml["info"]["name"] = basename(testDir)
            if not yaml.get("build"):
                 yaml["build"] = {}
            if not yaml.get("build").get("separate"):
                 yaml["build"]["separate"] = []
            # TODO...
     
        return yaml, msg


    #------------------#
    # Instance methods #
    #------------------#

    def __init__(self, dirPath):
        
        from common import fatalmsg
        
        if Test.isTestDir(dirPath):
            self.dirPath  = dirPath
            self.yamlRead = False
        else:
            fatalmsg("Test.__init__: dirPath must point to a valid test directory but does not ({})").format(dirPath)


    def path(self):
            
        return self.dirPath


    def yaml(self):
        
        if not self.yamlRead:
            self.yaml, self.yamlMsg = Test._readYaml(self.dirPath)
            self.yamlRead = True
            
        return self.yaml


    def yamlMsg(self):
        
        _ = self.yaml()     # ensure yaml has been read
        return self.yamlMsg
    
    




