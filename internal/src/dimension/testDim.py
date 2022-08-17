################################################################################
#                                                                              #
#  testDim.py                                                                  #
#  set of paths to test cases, constructed from "spec" exprs                   #
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




from . import StringDim


class TestDim(StringDim):
    
    @classmethod
    def name(cls):
        
        return "tests"
    
    
    @classmethod
    def default(cls):

        return "all"


    @classmethod
    def format(cls, value, forName=False):
        
        from os.path import relpath, join
        from common import homepath
        
        return value.replace("/", "--") if forName else value

    
    def __init__(self, spec, selftest=False):
        # 'spec' is a comma-separated list of Unix pathname patterns relative to $HPCTEST_HOME/tests
        
        from os.path import join, relpath                                                                                                                                                                                            
        from util.glob2 import iglob
        from common import options, homepath, infomsg
        from test import Test
        
        self.spec = spec
        
        testsPath    = join(homepath,  "tests")
        selftestPath = join(testsPath, "selftest")
        pendingPath  = join(testsPath, "pending")
        chosenTestsPath = selftestPath if selftest else testsPath
        
        self.valueList = []
        
        def appendIf(path):
            if path.startswith(selftestPath) == selftest:
               if not path.startswith(pendingPath):
                    self.valueList.append(path)

        if spec == "all":
            Test.forEachDo( lambda test: appendIf(test.path()) )
        else:
            for elem in (spec if isinstance(spec, list) else [spec]):
                for testPattern in elem.replace(',', ' ').split():
                    for path in iglob( join(chosenTestsPath, testPattern.strip()) ):
                        if Test.isTestDir(path):
                            appendIf(path)
                        else:
                            if "verbose" in options:
                                relativePath = relpath(path, testsPath)
                                infomsg("{} is not a test directory, will be ignored".format(relativePath))


    def values(self):
            
        return frozenset( list(map(self._makeTest, self.valueList)) )


    def __iter__(self):
        
        
        return map(self._makeTest, self.valueList)
        

    @staticmethod
    def _makeTest(path):
        
        from test import Test
        return Test(path)




