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

    
    def __init__(self):
        
        self.jobDescriptions = dict()
        self.runningJobs = set()
         
    
    # System inquiries

    _local_executor_class = None
    _local_executor       = None


    @classmethod
    def localExecutorClass(cls):
        
        import configuration, sys
        from common import yesno, infomsg, fatalmsg
        
        if not cls._local_executor_class:
            
            if configuration.get("config.batch.manager"):
                
                # local configuration specifies a job launcher
                name  = configuration.get("config.batch.manager")
                force = configuration.get("config.batch.debug.force", False)
                if name not in cls._subclasses:
                    fatalmsg("configuration specifies unknown config.batch.manager: {}".format(name))
                
                # validate the corresponding executor class
                executorClass = cls._subclasses[name]
                available, msg = executorClass.isAvailable()
                if not (available or force):
                    fatalmsg("config files specify {} as config.batch.manager, "
                             "but {}".format(name, msg if msg else  name + " is not available"))
                cls._local_executor_class = executorClass
            
            else:
                cls._local_executor_class = cls._subclasses["Shell"]
                
#        WORK IN PROGRESS:
#
#             else:
#                 
#                 def ask():
#                     ask    = "Do you want to continue without using batch?"
#                     cancel = "Ok, exiting. Edit config.batch to specify a manager if desired."
#                     return yesno(ask, cancel)
#             
#                 # see if a batch manager seems present even though none specified in config
#                 avail = {mgrClass for mgrClass in cls._subclasses.values()
#                                       if mgrClass.name() != "Shell" and mgrClass.isAvailable()[0]}
#                 if avail:
#                     availNames = [m.name() for m in avail]
#                     if len(avail) == 1:
#                         subject = "A {} batch manager".format(availNames[0])
#                         plural  = "s"   # sic!
#                     else:
#                         subject = "Batch managers " + ",".join(availNames[:-1]) + " and " + availNames[-1]
#                         plural  = ""   # sic!
#                         
#                     msg = "{} seem{} to be present, but no config.batch.manager is specified."  \
#                           .format(subject, plural)
#                     infomsg(msg)
#                     if not ask(): sys.exit()
#                     
#                 cls._local_executor_class = cls._subclasses["Shell"]

        return cls._local_executor_class
    
    
    @classmethod
    def localExecutor(cls):
        
        if not cls._local_executor:
            cls._local_executor = cls.localExecutorClass() ()
        
        return cls._local_executor
    
    
    @classmethod
    def name(cls):
        
        from common import subclassResponsibility
        subclassResponsibility("Executor", "name")
    

    @classmethod
    def defaultToBackground(cls):
        
        return cls.localExecutorClass().defaultToBackground()


    @classmethod
    def isAvailable(cls):                               # returns (available, msg_or_None)
        
        return cls.localExecutorClass().isAvailable()

    
    @classmethod
    def _checkCmdsAvailable(cls, cmdList):
        
        from common import whichDir
        
        missing = [cmd for cmd in cmdList if not whichDir(cmd)]
        if missing:
            ok, msg = False, ", ".join(missing) + " {} missing".format("are" if len(missing) > 1 else "is")
        else:
            ok, msg = True, None
        
        return ok, msg
        

    # Registry of available executor subclasses

    _subclasses = dict()


    @classmethod
    def register(cls, name, subclass):
        cls._subclasses[name] = subclass


    # Programming model support
    
    def wrap(self, cmd, runPath, binPath, numRanks, numThreads, spackMPIBin):
        
        # numRanks == 0 means don't use MPI
        # numThreads == 0 means don't use OpenMP
        
        subclassResponsibility("Executor", "wrap")


    # Scheduling operations
    
    def run(self, cmd, runPath, binPath, numRanks, numThreads, outPath, description):
        
        from common import subclassResponsibility
        subclassResponsibility("Executor", "run")

    
    def submitJob(self, cmd, prelude, numRanks, numThreads, name, description):   # returns jobID, out, err

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
        
        # general method; a subclass might override with more efficient specific one
        
        finished = set()
        
        for p in self.runningJobs:
            if self.isFinished(p):
                finished.add(p)
        
        for p in finished:
            self.runningJobs.remove(p)
        
        return finished

    
    def kill(self, job):
        
        from common import subclassResponsibility
        subclassResponsibility("Executor", "kill")
    
    
    def killAll(self):
        
        for p in self.runningJobs:
            p.kill()


    def _addJob(self, job, description):

        self.runningJobs.add(job)
        self.jobDescriptions[job] = description        


    def _removeJob(self, job):

        self.runningJobs.remove(job)
        self.jobDescriptions.pop(job)


    def _shell(self, cmd, binPath=None, runPath=None, outPath=None):
               
        import os, sys
        from subprocess import Popen, PIPE
        
        try:
            
            path = outPath if outPath else "/dev/stdout"
            with open(path, "w") as output:
                
                env = os.environ.copy()
                if binPath:
                    env["PATH"] = binPath + ":" + env["PATH"]
                
                proc = Popen(cmd, shell = True,
                                  env = env,
                                  cwd = runPath if runPath else os.getcwd(),
                                  stdout = PIPE, stderr = PIPE)
                out, err_out = proc.communicate()
                err = proc.returncode
                
                if not out:     out = ""
                if not err_out: err_out = ""
                if err: out = err_out.strip()
            
        except StandardError as e:
            out = e.strerror
            err = e.errno
        except Exception as e:
            out = str(e)
            err = -1   ## TODO: is there a better property of Exception to use for 'err'?
            
        return out, err
    







