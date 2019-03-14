################################################################################
#                                                                              #
#  slurmExecutor.py                                                            #
#                                                                              #
#  Run jobs immediately or in batch using the SLURM scheduler.                 #
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



from executor import Executor


class SlurmExecutor(Executor):
    
    
    def __init__(self):
        
        super(SlurmExecutor, self).__init__()
    

    @classmethod
    def defaultToBackground(cls):
        
        return True

    
    def run(self, cmd, runDirPath, env, outPath):
        
        from common import notImplemented
        
        notImplemented("SlurmExecutor.run")

    
    def submitJob(self, cmd, description):
        
        from common import notImplemented
        
        notImplemented("SlurmExecutor.submitJob")

    
    def isFinished(self, jobID):
        
        from common import notImplemented
        
        notImplemented("SlurmExecutor.isFinished")
        return True

    
    def pollForFinishedJobs(self):

        from common import notImplemented

        notImplemented("SlurmExecutor.pollForFinishedJobs")
        return { }

    
    def kill(self, process):

        from common import notImplemented

        notImplemented("SlurmExecutor.kill")

    
    def killAll(self):

        from common import notImplemented

        notImplemented("SlurmExecutor.killAll")


# register this executor class by name
Executor.register("Slurm", SlurmExecutor)



