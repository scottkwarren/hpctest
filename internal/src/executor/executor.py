################################################################################
#                                                                              #
#  executor.py                                                                 #
#                                                                              #
#  Run obs immediately or in batch/background using one of various supported   #
#  schedulers (defined elsewhere). Knows which schedulers are supported on the #
#  current system and whether to run jobs immediately or in batch by default.  #
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



#################################################
#  ABSTRACT SUPERCLASS                          #
#################################################


class Executor(object):

    
    # System inquiries

    @classmethod
    def localExecutorName(cls):
        
        import configuration
        from common import fatalmsg
                
        # local configuration may specify the job launcher
        name = configuration.get("config.batch.manager", "Shell")
        
        if name not in cls._subclasses:
            fatalmsg("config.yaml specifies unknown name '{}' for 'config.batch.manager'".format(name))
            
        return name


    @classmethod
    def defaultToBackground(cls):
        
        return cls._subclasses[cls.localExecutorName()].defaultToBackground()


    @classmethod
    def create(cls):
        
        import configuration

        # make an executor corresponding to the name specified by config or default
        name = configuration.get("config.batch.manager", "Shell")
        ex = cls._subclasses[name]()
        return ex


    # Registry of available executor subclasses

    _subclasses = dict()


    @classmethod
    def register(cls, name, subclass):
        
        cls._subclasses[name] = subclass


    # Scheduling operations
    
    def __init__(self):
        
         self.jobDescriptions = dict()
         
    
    def run(self, cmd, runDirPath, env, numRanks, numThreads, outPath, description):
        from common import subclassResponsibility
        subclassResponsibility("Executor", "run")
    
    def submitJob(self, cmd, runDirPath, env, numRanks, numThreads, outPath, description):   # returns jobID, errno
        from common import subclassResponsibility
        subclassResponsibility("Executor", "submitJob")
    
    def description(self, jobID):
        return self.jobDescriptions[jobID]
    
    def stdout(self, jobID):
        return self.jobStdouts[jobID]
                                    
    def isFinished(self, jobID):
        from common import subclassResponsibility
        subclassResponsibility("Executor", "isFinished")
    
    def waitFinished(self, jobID):
        import time
        while not self.isFinished(jobID): time.sleep(5)     # seconds
    
    def pollForFinishedJobs(self):
        from common import subclassResponsibility
        subclassResponsibility("Executor", "pollForFinishedJobs")
    
    def kill(self, process):
        from common import subclassResponsibility
        subclassResponsibility("Executor", "kill")
    
    def killAll(self):
        from common import subclassResponsibility
        subclassResponsibility("Executor", "killAll")








