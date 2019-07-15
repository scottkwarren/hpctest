################################################################################
#                                                                              #
#  profileDim.py                                                               #
#  set of param strings for hpc{run,struct,prof} constructed from "spec" exprs #
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


class ProfileDim(StringDim):
    
    @classmethod
    def name(cls):
        
        return "profile"
    
    
    @classmethod
    def default(cls):

        import configuration
        return ( configuration.get("profile.hpctoolkit.hpcrun params", "REALTIME@10000") +
                 ";" +
                 configuration.get("profile.hpctoolkit.hpcstruct params", "") +
                 ";" +
                 configuration.get("profile.hpctoolkit.hpcprof params", "")
               )


    @classmethod
    def format(cls, value, forName=False):
        
        stripped = value.rstrip(" ;")
        return stripped.replace(" ", ".").replace(";", ":") if forName else stripped

    
    def __init__(self, spec):
        # 'spec' is a comma-separated list of '+'-separated lists of metric-specs
        # such as 'REALTIME@10000 + IO@100 + MEMLEAK@10, CPUTIME@10000, WALLTIME@1000'
        
        self.valueList = \
            [ "-e " + metrics.replace("+", " -e ")
                for metrics in spec.split(',')
            ]


    # everything else is inherited from StringDim



