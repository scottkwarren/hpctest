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
from common import options


class SlurmExecutor(Executor):
    
    
    def __init__(self):
        
        super(SlurmExecutor, self).__init__()
        # nothing for SlurmExecutor
    

    @classmethod
    def defaultToBackground(cls):
        
        return True

    
    @classmethod
    def isAvailable(cls):
        
        from common import whichDir
        available = whichDir("srun") is not None and whichDir("sbatch") is not None
        return available, "srun and sbatch are missing"


    def run(self, cmd, runPath, env, numRanks, numThreads, outPath, description): # returns nothing, raises
        
        from common import ExecuteFailed
        out, err = _srun(cmd, runPath, env, numRanks, numThreads, outPath, description)
        if err:
            raise ExecuteFailed(out, err)

    
    def submitJob(self, cmd, env, numRanks, numThreads, outPath, name, description):   # returns jobID, out, err
        
        from common import ExecuteFailed

        jobid, out, err = _sbatch(cmd, env, numRanks, numThreads, outPath, name, description)
        if err == 0:
            self._addJob(jobid, description)
        
        return jobid, out, err

    
    def isFinished(self, jobID):
        
        return False    ## TODO: DEBUG

    
    def pollForFinishedJobs(self):
        
        import os, re
        
        # ask Slurm for all our jobs that are still running
        userid = os.environ["USER"]
        out, err = _shell("squeue --user={} --noheader".format(userid))
        
        # start with all remaining jobs and remove ones mentioned by 'squeue' and hence still running
        finished = self.runningJobs.copy()
        for line in out.splitlines():
            match = re.match(r" *([0-9]+) ", line)
            if match:
                jobid = match.group(1)
                finished.remove(jobid)
            else:
                errormsg("unexpected output from 'squeue':\n {}".format(out))
        
        # clean up finished jobs
        for p in finished:
            self.runningJobs.remove(p)
        
        return finished

    
    def kill(self, process):

        return    ## TODO: DEBUG




def _shell(cmd):
           
    import subprocess
    
    try:
        
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err_out = proc.communicate()
        err = proc.returncode
        if err: out = err_out.strip()
        
    except StandardError as e:
        out = e.strerror
        err = e.errno
    except Exception as e:
        out = str(e)
        err = -1   ## TODO: is there a better property of Exception to use for 'err'?
        
    return out, err


def _srun(cmd, runPath, env, numRanks, numThreads, outPath, description): # returns (out, err)
    
    from os import getcwd
    import textwrap, tempfile
    from pipes import quote
    from common import options, verbosemsg
    
    # slurm srun command template
    Slurm_run_cmd_template = textwrap.dedent(
        "srun {options} "
        "     --account={account} "
        "     --partition={partition} "
        "     --chdir={runPath} "
        "     --export=\"{env}\" "
        "     --exclusive "
        "     --ntasks={numRanks} "
        "     --cpus-per-task={numThreads} "
        "     --time={time} "
        "     --mail-type=NONE "
        "     {cmd}"
        )

    # template params from configuration
    account, partition, time = _paramsFromConfiguration()

    # prepare slurm command
    cmd = Slurm_run_cmd_template.format(
        options      = "--verbose" if "debug" in options else "",
        account      = account,
        partition    = partition,
        runPath      = runPath,
        env          = quote(str(env)),
        numRanks     = numRanks,
        numThreads   = numThreads,
        time         = time,
        cmd          = cmd
        )
    
    # run the command immediately with 'srun'
    verbosemsg("Executing via srun:\n{}".format(cmd))
    out, err = _shell(cmd)
    
    return out, (err if err else 0)


def _sbatch(cmd, env, numRanks, numThreads, outPath, name, description): # returns (jobid, out, err)
    
    import textwrap, tempfile
    from os import getcwd
    import re
    from pipes import quote
    import common
    from common import verbosemsg, errormsg
    
    # slurm sbatch command file template
    Slurm_batch_file_template = textwrap.dedent(
        """\
        #!/bin/bash
        #SBATCH --job-name={jobName}
        #SBATCH --account={account}
        #SBATCH --partition={partition}
        #SBATCH --export=\"{env}\"
        #SBATCH --exclusive
        #SBATCH --ntasks={numRanks}
        #SBATCH --cpus-per-task={numThreads}
        #SBATCH --time={time}
        #  #SBATCH --output={outPath}
        #SBATCH --mail-type=NONE
        {cmd} 
        """)

    # template params from configuration
    account, partition, time = _paramsFromConfiguration()
    
    # prepare slurm command file
    f = tempfile.NamedTemporaryFile(mode='w+t', bufsize=-1, delete=False,
                                    dir=getcwd(), prefix='sbatch-', suffix=".slurm")
    f.write(Slurm_batch_file_template.format(
        jobName      = name,
        account      = account,
        partition    = partition,
        env          = quote(str(env)),
        numRanks     = numRanks,
        numThreads   = numThreads,
        time         = time,
        outPath      = outPath,     # commented out in template
        cmd          = cmd,
        ))
    f.close()
    
    # submit command file for batch execution with 'sbatch'
    options = "--verbose " if "debug" in common.options else ""
    command = "    sbatch {}{}".format(options, f.name)
    
    verbosemsg("submitting job {} ...".format(description))
    verbosemsg("    " + command)
    
    out, err = _shell(command)
    
    verbosemsg("    " + out)
    verbosemsg("\n")
    
    # handle output from submit command
    if err:
        jobid = None
    else:
        # extract job id from 'out'
        match = re.match(r".* ([0-9]+)$", out)
        if match:
            jobid = match.group(1)
        else:
            jobid = None
            err = "unexpected output from 'sbatch': {}".format(out)
            errormsg(err)
    
    return (jobid, out, err if err else 0)


def _paramsFromConfiguration():
    
    import configuration

    account   =  configuration.get("batch.params.account",   "commons")
    partition =  configuration.get("batch.params.partition", "commons")
    time      =  configuration.get("batch.params.time",      "1:00:00")
    
    return (account, partition, time)




# register this executor class by name
Executor.register("Slurm", SlurmExecutor)





