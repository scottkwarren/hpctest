################################################################################
#                                                                              #
#  batch.py                                                                    #
#  knows whether current system uses batch scheduling, which batch scheduler   #
#  if so, and how to use each supported scheduler                              #
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



#######################
# ABSTRACT SUPERCLASS #
#######################


class Executor():

    
    # System inquiries

    @classmethod
    def batchInUse(cls):
        
        import configuration
        return configuration.get("local.batch", None) is not None
    
    
    @classmethod
    def scheduler(cls, wantBatch):
        
        import configuration
        
        name = configuration.get("local.batch", None)

        if name == "Shell":
            scheduler = ShellBatch if wantBatch else ShellImmediate
        elif name == "Slurm":
            scheduler = SlurmBatch if wantBatch else SlurmImmediate
        else:
            scheduler = None
            
        return scheduler


    # Scheduling operations
    
    def __init__(self):
        
        pass
    
    
    def launch(self, cmd):
        
        from common import subclassResponsibility
        subclassResponsibility("Batch", "launch")
    
    
    def isFinished(self, jobID):
        
        from common import subclassResponsibility
        subclassResponsibility("Batch", "isFinished")
    
    
    def waitFinished(self, jobID):
        
        import time
        while not self.isFinished(jobID): time.sleep(5)     # seconds
    
    
    def pollForFinishedRuns(self):
        
        from common import subclassResponsibility
        subclassResponsibility("Batch", "pollForFinishedRuns")




###########################
# SHEL IMMEDIATE EXECUTOR #
###########################


class ShellImmediate():

    
    def __init__(self):
        
        super().__init__()
    
    
    def launch(self, cmd):
        
        pass
    
    
    def isFinished(self, jobID):
        
        return True
    
    
    def pollForFinishedRuns(self):
        
        return { }




########################
# SHELL BATCH EXECUTOR #
########################


class ShellBatch(Executor):

    
    def __init__(self):
        
        super().__init__()
    
    
    def launch(self, cmd):
        
        pass
    
    
    def isFinished(self, jobID):
        
        return True
    
    
    def pollForFinishedRuns(self):
        
        return { }




############################
# SLURM IMMEDIATE EXECUTOR #
############################


class SlurmImmediate(Executor):

    
    def __init__(self):
        
        super().__init__()
    
    
    def launch(self, cmd):
        
        pass
    
    
    def isFinished(self, jobID):
        
        return True
    
    
    def pollForFinishedRuns(self):
        
        return { }




########################
# SLURM BATCH EXECUTOR #
########################


class SlurmBatch(Executor):

    
    def __init__(self):
        assertMessage(Executor.batchInUse(), "tried to make a SlurmBatch executor but batch is not im use.")
        super().__init__()
    
    
    def launch(self, cmd):
        
        pass
    
    
    def isFinished(self, jobID):
        
        return True
    
    
    def pollForFinishedRuns(self):
        
        return { }





