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
        available = whichDir("srun") and whichDir("sbatch")
        return available, "srun and sbatch are missing"


    def run(self, cmd, runPath, env, numRanks, numThreads, outPath, description): # returns nothing, raises
        
        # 'env' arg ignored! What if higher levels need to add to environment??
        
        from common import ExecuteFailed
        out, err = self._srun(cmd, runPath, env, numRanks, numThreads, outPath, description)
        if err:
            raise ExecuteFailed(out, err)

    
    def submitJob(self, cmd, env, numRanks, numThreads, outPath, name, description):   # returns jobID, out, err
        
        # 'env' arg ignored! What if higher levels need to add to environment??
        
        from common import ExecuteFailed

        jobid, out, err = self._sbatch(cmd, env, numRanks, numThreads, outPath, name, description)
        if err == 0:
            self._addJob(jobid, description)
        
        return jobid, out, err

    
    def isFinished(self, jobID):
        
        return False    ## TODO: DEBUG

    
    def pollForFinishedJobs(self):
        
        import os, re
        
        # ask Slurm for all our jobs that are still running
        userid = os.environ["USER"]
        out, err = self._shell("squeue --user={} --noheader".format(userid))
        
        # 'out' is a possibly-empty sequence of lines that look like this:
        # '           278061   commons app--lul  skw0897  R       9:53      1 c1'


        # compute the set of jobs finished since last poll:
        # start with all previously-running jobs and remove the ones still running per 'squeue'
        finished = self.runningJobs.copy()
        for line in out.splitlines():
            # match the job id, the first nonblank character (digit) sequence on the line
            match = re.match(r" *([0-9]+) ", line)
            if match:
                jobid = match.group(1)
                if jobid in finished:
                    finished.remove(jobid)
            else:
                errormsg("unexpected output from squeue:\n {}".format(out))
        
        # clean up finished jobs
        for p in finished:
            self.runningJobs.remove(p)
        
        return finished

    
    def kill(self, jobid):

        out, err = self._shell("scancel {}".format(jobid))
        if err != 0:
            errormsg("attempt to cancel batch job {} failed".format(jobid))


    def _srun(self, cmd, runPath, env, numRanks, numThreads, outPath, description): # returns (out, err)
        
        # 'env' arg ignored! What if higher levels need to add to environment??
        from os import getcwd
        import textwrap, tempfile
        import common
        from common import options, verbosemsg
        
        # slurm srun command template
        if common.args["_runOne"]:   # now running nested in a batch script
            Slurm_run_cmd_template = textwrap.dedent(
                "srun {options} "
                "     --chdir={runPath} "
                "     {cmd}"
                )
        else:
            Slurm_run_cmd_template = textwrap.dedent(
                "srun {options} "
                "     --account={account} "
                "     --partition={partition} "
                "     --time={time} "
                "     --exclusive "
                "     --chdir={runPath} "
                "     --ntasks={numRanks} "
                "     --cpus-per-task={numThreads} "
                "     --mail-type=NONE "
                "     {cmd}"
                )
    
        # template params from configuration
        account, partition, time = self._paramsFromConfiguration()
    
        # prepare slurm command
        scommand = Slurm_run_cmd_template.format(
            options      = "--slurmd-debug=verbose" if "debug" in options else "",
            account      = account,
            partition    = partition,
            time         = time,
            runPath      = runPath,
            numRanks     = numRanks,
            numThreads   = numThreads,
            cmd          = cmd
            )
        
        # run the command immediately with 'srun'
        verbosemsg("Executing via srun:\n{}".format(scommand))
        out, err = self._shell(scommand)
        
        return out, (err if err else 0)


    def _sbatch(self, cmds, env, numRanks, numThreads, outPath, name, description): # returns (jobid, out, err)
        
        # 'env' arg ignored! What if higher levels need to add to environment??
        
        import textwrap, tempfile
        from os import getcwd
        from os.path import join
        import re
        import common
        from common import options, verbosemsg, errormsg
        
        # slurm sbatch command file template
        Slurm_batch_file_template = textwrap.dedent(
            """\
            #!/bin/bash
            #SBATCH --job-name={jobName}
            #SBATCH --account={account}
            #SBATCH --partition={partition}
            #SBATCH --exclusive
            #SBATCH --ntasks={numRanks}
            #SBATCH --cpus-per-task={numThreads}
            #SBATCH --time={time}
            #SBATCH --mail-type=NONE
            export OMP_NUM_THREADS={numThreads}
            {cmds} 
            """)
    
        # template params from configuration
        account, partition, time = self._paramsFromConfiguration()
        
        # prepare slurm command file
        slurmfilesDir = getcwd() if "debug" in options else join(common.homepath, ".hpctest")
        f = tempfile.NamedTemporaryFile(mode='w+t', bufsize=-1, delete=False,
                                        dir=slurmfilesDir, prefix='slurm-', suffix=".sbatch")
        f.write(Slurm_batch_file_template.format(
            jobName       = name,
            account       = account,
            partition     = partition,
            numRanks      = numRanks,
            numThreads    = numThreads,
            time          = time,
            outPath       = outPath,     # commented out in template
            cmds          = cmds,
            ))
        f.close()
        
        # submit command file for batch execution with 'sbatch'
        sbatchOpts = "--slurmd-debug=verbose" if "debug" in options else "",
        scommand = "sbatch {}{}".format(sbatchOpts, f.name)
        
        verbosemsg("submitting job {} ...".format(description))
        verbosemsg("    " + scommand)
        
        out, err = self._shell(scommand)
        
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
                err = "unexpected output from sbatch: {}".format(out)
                errormsg(err)
        
        return (jobid, out, err if err else 0)
        



# register this executor class by name
Executor.register("Slurm", SlurmExecutor)





