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



#################################################
#  ABSTRACT SUPERCLASS                          #
#################################################


class Executor(object):

    
    # System inquiries

    @classmethod
    def create(cls):
        
        import configuration
                
        # local configuration specifies the job launcher if any
        name = configuration.get("config.batch.manager", "Shell")

        # make corresponding executor
        if name == "Shell":
            ex = ShellExecutor()
        elif name == "Slurm":
            ex = SlurmExecutor()
        else:
            fatalmsg("config.yaml gives invalid name '{}' for config.batch.manager".format(name))
            
        return ex


    # Scheduling operations
    
    def __init__(self):
        
         self.jobDescriptions = dict()
         
    
    def defaultToBackground(cls):
        from common import subclassResponsibility
        subclassResponsibility("Executor", "defaultTobackground")

    def run(self, cmd, runDirPath, env, outPath):
        from common import subclassResponsibility
        subclassResponsibility("Executor", "launch")
    
    def submitJob(self, cmd, description):
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




#################################################
#  SHELL EXECUTOR                               #
#################################################


class ShellExecutor(Executor):

    
    def __init__(self):
        
        super(ShellExecutor, self).__init__()
        self.runningProcesses = set()

    
    def defaultToBackground(cls):

        return False


    def run(self, cmd, runDirPath, env, outPath):
        
        import os
        from subprocess import call, CalledProcessError
        from common import ExecuteFailed
           
        try:
               
            if runDirPath:
                oldwd  = os.getcwd()
                os.chdir(runDirPath)
                
            with open(outPath, "w") as output:
                call(cmd, shell=True, stdin=None, stdout=output, stderr=output, env=env)
              
        except CalledProcessError as e:
            raise ExecuteFailed(str(e), "exit status %d" % process.returncode)
        except OSError as e:
            raise ExecuteFailed('%s: %s' % (self.exe[0], e.strerror))
        except Exception as e:
            raise ExecuteFailed(e.message)
        
        finally:
            if runDirPath: os.chdir(oldwd)
    
    
    def submitJob(self, cmd, description):
                
        from StringIO import StringIO
        import subprocess
        from subprocess import Popen, CalledProcessError
        from common import ExecuteFailed
        
        try:
            
            process = Popen(cmd, shell=True, stdin=None)

        except OSError as e:
            raise ExecuteFailed('%s: %s' % (self.exe[0], e.strerror))
        except CalledProcessError as e:
            raise ExecuteFailed(str(e), "exit status %d" % process.returncode)
            
        self.runningProcesses.add(process)
        self.jobDescriptions[process] = description        

        return process
    
    
    def isFinished(self, process):
        
        return process.poll() != None
    
    
    def pollForFinishedJobs(self):
        
        finished = set()
        for p in self.runningProcesses:
            if p.poll() != None:
                finished.add(p)
        for p in finished:
            self.runningProcesses.remove(p)
        return finished
    
    
    def kill(self, process):
        
        process.kill()
        self._cleanup(process)
    
    
    def killAll(self):
        
        for p in self.runningProcesses:
            p.kill()


    def _cleanup(self, process):

        self.runningProcesses.remove(process)
        self.jobDescriptions.pop(process)



#################################################
#  SLURM EXECUTOR                               #
#################################################


class SlurmExecutor(Executor):

    
    def __init__(self):
        
        super(SlurmExecutor, self).__init__()
    
    
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





