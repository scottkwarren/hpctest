################################################################################
#                                                                              #
#  shellExecutor.py                                                            #
#                                                                              #
#  Run jobs immediately or in background using the shell.                      #
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


class ShellExecutor(Executor):

    
    def __init__(self):
        
        super(ShellExecutor, self).__init__()
        self.runningProcesses = set()

    
    @classmethod
    def defaultToBackground(cls):
        
        return False

    
    def run(self, cmd, runPath, env, outPath, description):
        
        import os
        from subprocess import call, CalledProcessError
        from common import ExecuteFailed
           
        try:
               
            if runPath:
                oldwd  = os.getcwd()
                os.chdir(runPath)
                
            with open(outPath, "w") as output:
                call(cmd, shell=True, stdin=None, stdout=output, stderr=output, env=env)
              
        except CalledProcessError as e:
            raise ExecuteFailed(str(e), "exit status %d".format(process.returncode))   ## <<< FIXME: iterate.doForAll must handle whatever's here
        except OSError as e:
            raise ExecuteFailed('{}: {}'.format(self.exe[0], e.strerror))   ## <<< FIXME: iterate.doForAll must handle whatever's here
        except Exception as e:
            raise ExecuteFailed(e.message)
        
        finally:
            if runPath: os.chdir(oldwd)
    
    
    def submitJob(self, cmd, runPath, env, outPath, description):   # returns jobID, errno
                
        from StringIO import StringIO
        import subprocess
        from subprocess import Popen, CalledProcessError
        from common import ExecuteFailed
        
        errno = 0
        try:
            
            if runPath:
                oldwd  = os.getcwd()
                os.chdir(runPath)

            process = Popen(cmd, shell=True, stdin=None, stdout=outPath, env=env)

        except OSError as e:
            errno = e.errno    # to return from 'submitjob'
            raise ExecuteFailed('%s: %s' % (self.exe[0], e.strerror))  ## <<< FIXME: iterate.doForAll must handle whatever's here
        except CalledProcessError as e:
            raise ExecuteFailed(str(e), "exit status %d" % process.returncode)  ## <<< FIXME: DITTO
        
        finally:
            if runPath: os.chdir(oldwd)
            
        self.runningProcesses.add(process)
        self.jobDescriptions[process] = description        

        return process, errno
    
    
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


# register this executor class by name
Executor.register("Shell", ShellExecutor)




