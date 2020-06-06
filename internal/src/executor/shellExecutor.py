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

    
    # System inquiries

    @classmethod
    def name(cls):
        
        return "Shell"


    @classmethod
    def isAvailable(cls):
        
        from common import whichDir
        available, msg = Executor._checkCmdsAvailable(["bash"])
        available = available or configuration.get("batch.debug.force", False)
        return available, "bash is missing"
    

    @classmethod
    def defaultToBackground(cls):
        
        return False

    
    # Programming model support
    
    def wrap(self, cmd, runPath, binPath, numRanks, numThreads, spackMPIBin):
        
        if numRanks:
            cmd = "{}/mpirun -np {} {}".format(spackMPIBin, numRanks, cmd)

        return cmd

    
    def run(self, cmd, runPath, binPath, numRanks, numThreads, outPath, description):   # returns nothing, raises
        
        import os, sys
        from subprocess import check_call, CalledProcessError
        from common import ExecuteFailed
           
        env = os.environ.copy()
        env["PATH"] = binPath + ":" + env["PATH"]
        env["OMP_NUM_THREADS"] = str(numThreads if numThreads > 0 else 1)
        
        # run the specified command
        try:
               
            if runPath:
                oldwd  = os.getcwd()
                os.chdir(runPath)
            
            with open(outPath, "w") as output:
                with open(outPath + ".err", "w") as error:
                    check_call(cmd, shell=True, stdin=None, stdout=output, stderr=error, env=env)
        
        except CalledProcessError as e:
            raise ExecuteFailed(self._shellError(e.returncode), e.returncode)
        except OSError as e:
            msg = "{}: {}".format(self.exe[0], e.strerror)
            raise ExecuteFailed(msg)
        except Exception as e:
            raise ExecuteFailed(e.message)
        finally:
            if runPath:
                os.chdir(oldwd)

    
    def submitJob(self, cmd, prelude, numRanks, numThreads, name, description):   # returns jobID, out, err
        
        import os
        from subprocess import Popen, CalledProcessError
        from common import ExecuteFailed

        # add the prelude commands if any
        if type(prelude) is not list: prelude = [prelude]
        cmd = "\n".join(prelude) + ("\n" if len(prelude) else "") + cmd
        
        env = os.environ.copy()
        err = 0
        try:
            
            process = Popen(cmd, shell=True, env=env)
            out     = ""
            err     = process.returncode

        except StandardError as e:
            out = e.strerror
            err = e.errno
            raise ExecuteFailed("{}: {})".format(self.exe[0], out), err)
        except CalledProcessError as e:
            out = str(e)
            err = process.returncode
            raise ExecuteFailed(out, err)
            
        self._addJob(process, description)
        
        return process, out, err
    
    
    def isFinished(self, process):
        
        p = process.poll()
        return p != None

    
    def kill(self, job):
        
        process.kill()
        self._removeJob(job)

    
    def _shellError(self, retcode):
        
        # see http://www.tldp.org/LDP/abs/html/exitcodes.html
        
        if retcode is 2:
            msg = "command faailed with incorrect usage"
        elif retcode < 126:
            msg = "command failed".format(retcode)
        elif retcode is 126:
            msg = "Command file is not executable"
        elif retcode is 127:
            msg = "Command file not found"
        elif retcode is 130:
            msg = "Command terminated by control-c"
        else:
            msg = "Command failed with fatal error signal {}".format(retcode-128)
        
        return msg
    

# register this executor class by name
Executor.register("Shell", ShellExecutor)




