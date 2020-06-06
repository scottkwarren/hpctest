################################################################################
#                                                                              #
#  stringDim.py                                                                #
#  abstract superclass for sets of strings constructed from "spec" exprs       #
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




from . import Dimension


class StringDim(Dimension):
    
    @classmethod
    def name(cls):
        
        from common import subclassResponsibility
        subclassResponsibility("StringDim", "name")
    
    
    @classmethod
    def default(cls):
        from common import subclassResponsibility
        subclassResponsibility("StringDim", "default")
        return None
    
    
    @classmethod
    def defaultDim(cls):
        
        return cls(cls.default())


    @classmethod
    def format(self, value, forName=False):
        
        return value

    
    def __init__(self, spec=""):
        
        self.spec = spec
        
        # TODO: quotes not yet supported
        if spec is None:
            self.valueList = []
        else:
            self.valueList = [ s.strip() for s in spec.split(",") ]


    def spec(self):
        
        return self.spec
    

    def isEmpty(self):
        
        return len(self.valueList) == 0


    def values(self):
            
        return frozenset(self.valueList)


    def __iter__(self):
        
        return iter(self.valueList)
