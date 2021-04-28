################################################################################
#                                                                              #
#  hpctkitDim.py                                                               #
#  set of paths to HPCTkit installs, constructed from "spec" exprs             #
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


class HPCTkitDim(StringDim):
    
    # TODO: implement short names for a configured set of HPCToolkit instances
    # TODO: validate each path to ensure it is a valid HPCToolkit install directory

    
    def __init__(self, spec=""):
        
        from common import is_path_valid, assertmsg;
        
        super(HPCTkitDim, self).__init__(spec);
        
        for s in self.valueList:
            assertmsg(is_path_valid(s),
                      "invalid path '{}' for new HPCTkitDim instance".format(s));

    
    @classmethod
    def name(cls):
        
        return "hpctoolkit"
    
    
    @classmethod
    def default(cls):

        from common import hpctk_default
        return hpctk_default


    # everything else is inherited from StringDim




