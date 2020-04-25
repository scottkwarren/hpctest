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
        from glob import glob
        from common import options, homepath, infomsg
        from test import Test
                  
        self.valueList = []
        if spec == "all":
            Test.forEachDo( lambda test: self.valueList.append(test.path()) )
        else:
            testsDir = join(homepath, "tests/selftest" if selftest else "tests")
            for elem in (spec if isinstance(spec, list) else [spec]):
                for testPattern in elem.replace(',', ' ').split():
                    for path in glob( join(testsDir, testPattern.strip()) ):
                        if Test.isTestDir(path)                                 \
                            and (selftest or not path.startswith(testsDir + "/selftest"))    \
                            and not path.startswith(testsDir + "/pending"):
                                self.valueList.append(path)
                        else:
                            if "verbose" in options:
                                relativePath = relpath(path, testsDir)
                                infomsg("{} is not a test directory, will be ignored".format(relativePath))


    def values(self):
            
        return frozenset( map(self._makeTest, self.valueList) )


    def __iter__(self):
        
        from itertools import imap
        return imap(self._makeTest, self.valueList)
        

    @staticmethod
    def _makeTest(path):
        
        from test import Test
        return Test(path)




