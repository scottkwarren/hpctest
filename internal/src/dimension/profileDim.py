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

from collections import namedtuple
ProfileArgs = namedtuple("ProfileArgs", "hpcrun hpcstruct hpcprof")


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
    def format(cls, prof, forName=False):
        
        fmt = ""
        if prof.hpcrun:    fmt +=       prof.hpcrun
        if prof.hpcstruct: fmt += ":" + prof.hpcstruct
        if prof.hpcprof:   fmt += ":" + prof.hpcprof
        if forName:        fmt  = fmt.replace(" ", ".").replace("-", "_")
        
        return fmt

    
    def __init__(self, spec):
        # 'spec' is a comma-separated list of '+'-separated lists of metric-specs
        # such as 'REALTIME@10000 + IO@100 + MEMLEAK@10, CPUTIME@10000, WALLTIME@1000'
        
        self.spec = spec
        
        # remove encoding tricks
        spec = spec.replace("_", "-").replace(".", " ")         # cmd line parser workaround
        spec = spec.strip(" ;:").replace(";", ":")              # run/struct/prof grouping
        spec = spec.replace("+", " ")                           # hpcrun event shortcuts
        
        # convert each three-part spec to a ProfileArgs tuple with formatted hpcrun string
        self.valueList = []
        for options in spec.split(','):
            runSpec, structSpec, profSpec = (options.split(":") + ["", ""])[:3]  # ensure len(rhs) == 3
            runString = ""
            prevWasMinus = False
            for opt in runSpec.split():
                if opt.startswith("-"):
                    runString += opt + " "
                    prevWasMinus = True
                else:
                    if not prevWasMinus: runString += "-e" + " "
                    runString += opt + " "
                    prevWasMinus = False
            runString = runString.strip()
            prof = ProfileArgs(runString, structSpec, profSpec)
            self.valueList.append(prof)


    # everything else is inherited from StringDim



