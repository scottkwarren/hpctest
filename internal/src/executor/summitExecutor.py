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


# First draft, based on the information in:
#    "Summit jsrun Introduction" (slides) by Chris Fuson
#     OLCF February User Call, February 28, 2018
#     https://www.olcf.ornl.gov/wp-content/uploads/2018/02/SummitJobLaunch.pdf
#
# LSF User;s Guide:
#     https://tin6150.github.io/psg/3rdParty/lsf4_userGuide/users-title.html


from executor import Executor
from common import options


class SummitExecutor(Executor):
    
    def __init__(self):
        
        super(SummitExecutor, self).__init__()
        # nothing for SummitExecutor
    

    @classmethod
    def defaultToBackground(cls):
        
        return True

    
    @classmethod
    def isAvailable(cls):
        
        from common import whichDir
        available = whichDir("jsrun") and whichDir("bsub")
        return available, "jsrun and bsub are missing"


    def run(self, cmd, runPath, env, numRanks, numThreads, outPath, description): # returns nothing, raises
        
        from common import ExecuteFailed
        out, err = self._jsrun(cmd, runPath, env, numRanks, numThreads, outPath, description)
        if err:
            raise ExecuteFailed(out, err)

    
    def submitJob(self, cmd, env, numRanks, numThreads, outPath, name, description):   # returns jobID, out, err
        
        from common import ExecuteFailed

        jobid, out, err = self._bsub(cmd, env, numRanks, numThreads, outPath, name, description)
        if err == 0:
            self._addJob(jobid, description)
        
        return jobid, out, err

    
    def isFinished(self, jobID):
        
        return False    ## TODO: DEBUG

    
    def pollForFinishedJobs(self):
        
        import os, re
        
        # ask Summit for all our jobs that are still running
        userid = os.environ["USER"]
        out, err = self._shell("bjobs -UF") # UF == "don't format output", makes parsing easier
        
        # 'out' is a sequence of lines that look like this:
        #
        # % bjobs 
        # JOBID USER     STAT  QUEUE      FROM_HOST   EXEC_HOST   JOB_NAME   SUBMIT_TIME
        # 3926  user1    RUN   priority   hostF        hostC      verilog    Oct 22 13:51
        # 605   user1    SSUSP idle       hostQ        hostC      Test4      Oct 17 18:07
        # 1480  user1    PEND  priority   hostD                   generator  Oct 19 18:13
        # 7678  user1    PEND  priority   hostD                   verilog    Oct 28 13:08
        # 7679  user1    PEND  priority   hostA                   coreHunter Oct 28 13:12
        # 7680  user1    PEND  priority   hostB                   myjob      Oct 28 13:17


        # compute the set of jobs finished since last poll:
        # start with all previously-running jobs and remove the ones still running per 'squeue'
        finished = self.runningJobs.copy()
        for line in out.splitlines()[1:]:    # skip header line
            # match the job id, the first nonblank character (digit) sequence on the line
            match = re.match(r" *([0-9]+) ", line)
            if match:
                jobid = match.group(1)
                if jobid in finished:
                    finished.remove(jobid)
            else:
                errormsg("unexpected output from bjobs:\n {}".format(out))
        
        # clean up finished jobs
        for p in finished:
            self.runningJobs.remove(p)
        
        return finished

    
    def kill(self, jobid):

        out, err = _shell("bkill {}".format(jobid))
        if err != 0:
            errormsg("attempt to kill batch job {} failed".format(jobid))


    def _jsrun(self, cmds, runPath, env, numRanks, numThreads, outPath, description): # returns (out, err)
        
        from os import getcwd
        import textwrap, tempfile
        from common import options, verbosemsg
        
        # slurm srun command template
        if common.args["_runOne"]:   # now running nested in a batch script
            Summit_run_cmd_template = textwrap.dedent(
                "srun {options} "
                "     --chdir={runPath} "
                "     {cmd}"
                )
        else:
            Summit_run_cmd_template = textwrap.dedent(
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
    
        # prepare summit command
        scommand = Summit_run_cmd_template.format(
            options      = "--verbose" if "debug" in options else "",
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
        
        # 'env' is ignored
        
        import textwrap, tempfile
        from os import getcwd
        from os.path import join
        import re
        import common
        from common import options, verbosemsg, errormsg
        
        # slurm sbatch command file template
        Summit_batch_file_template = textwrap.dedent(
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
        summitfilesDir = getcwd() if "debug" in options else join(common.homepath, ".hpctest")
        f = tempfile.NamedTemporaryFile(mode='w+t', bufsize=-1, delete=False,
                                        dir=summitfilesDir, prefix='summit-', suffix=".bsub")
        f.write(Summit_batch_file_template.format(
            jobName      = name,
            account      = account,
            partition    = partition,
            numRanks     = numRanks,
            numThreads   = numThreads,
            time         = time,
            outPath      = outPath,     # commented out in template
            cmds         = cmds,
            ))
        f.close()
        
        # submit command file for batch execution with 'sbatch'
        bsubOpts = "--verbose" if "debug" in options else ""
        scommand = "bsub {} < {}".format(bsubOpts, f.name)
        
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
            match = re.match(r".*([0-9]+)$", out)
            if match:
                jobid = match.group(1)
            else:
                jobid = None
                err = "unexpected output from bsub: {}".format(out)
                errormsg(err)
        
        return (jobid, out, err if err else 0)
    



# register this executor class by name
Executor.register("Summit", SummitExecutor)





