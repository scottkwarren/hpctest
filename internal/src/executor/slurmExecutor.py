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
        
    
    # System inquiries

    @classmethod
    def isAvailable(cls):
        
        from common import whichDir
        import configuration
        
        available, msg = Executor._checkCmdsAvailable(["srun", "sbatch", "squeue"])
        available = available or configuration.get("batch.debug.force")
        
        return available, msg


    @classmethod
    def defaultToBackground(cls):
        
        return True

    
    # Programming model support
    
    def wrap(self, cmd, runPath, env, numRanks, numThreads, spackMPIBin):
        
        # 'spackMPIBin' is unused
        
        from common import args, options
        
        # get template
        if args["_runOne"]:   # now running nested in a batch script
            if numRanks == 0:
                Slurm_run_cmd_template = "srun {options} --ntasks=1 {cmd}"
            else:
                Slurm_run_cmd_template = "srun {options} {cmd}"
        else:
            Slurm_run_cmd_template = textwrap.dedent(
                "srun {options} "
                "     --account={account} "
                "     --partition={partition} "
                "     --time={time} "
                "     --exclusive "
                "     --ntasks={numRanks} "
                "     --cpus-per-task={numThreads} "
                "     --mail-type=NONE "
                "     {cmd}"
                )
        
        # insert parameters
        account, partition, time = self._paramsFromConfiguration()
        srunCmd = Slurm_run_cmd_template.format(
            options      = "--verbose" if "debug" in options else "",
            account      = account,
            partition    = partition,
            time         = time,
            numRanks     = numRanks if numRanks > 0 else 1,
            numThreads   = numThreads,
            cmd          = cmd
            )

        # replace newlines by spaces, multiple spaces by one
        srunCmd = " ".join(srunCmd.split())
        
        return srunCmd
#------------------------------------------------------------------------------

    
    # Scheduling operations
    
    def run(self, cmd, runPath, env, numRanks, numThreads, outPath, description): # returns nothing, raises
        
        # assumes that 'cmd' has been "wrapped" appropriately
        
        from common import ExecuteFailed, verbosemsg
        
        verbosemsg("Running this command:\n{}".format(cmd))
        out, err = self._shell(cmd, env, runPath, outPath)
        
        if err: raise ExecuteFailed(out, err)

    
    def submitJob(self, cmd, env, numRanks, numThreads, outPath, name, description):   # returns jobID, out, err
        
        from common import ExecuteFailed

        jobid, out, err = self._sbatch(cmd, env, numRanks, numThreads, outPath, name, description)
        if err == 0:
            self._addJob(jobid, description)
        
        return jobid, out, err

    
    def isFinished(self, jobID):
        
        return False    ## TODO: DEBUG

    
    def pollForFinishedJobs(self):
        
        import os, re
        from common import errormsg, fatalmsg
        
        # ask Slurm for all our jobs that are still running
        userid = os.environ["USER"]
        out, err = self._shell("squeue --user={} --noheader".format(userid))
        if err: fatalmsg("can't invoke 'squeue' to poll for unfinished jobs")
        
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


    def _sbatch(self, cmds, env, numRanks, numThreads, outPath, name, description): # returns (jobid, out, err)
        
        # 'env' is ignored
        
        import textwrap, tempfile
        from os import getcwd
        from os.path import join
        import os, re
        import common
        from common import options, verbosemsg, debugmsg, errormsg
                
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
        sbatchOpts = "--verbose" if "debug" in options else ""
        scommand = "sbatch {} {}".format(sbatchOpts, f.name)
        
        verbosemsg("submitting job {} ...".format(description))
        verbosemsg("    " + scommand)
        
        out, err = self._shell(scommand)
        
        verbosemsg("    " + out)
        verbosemsg("\n")
        
        # handle output from submit command
        # ... apparently looks like this (see tinyurl.com/wuh7rtg):
        # Submitted batch job 5278683
        
        # handle output from submit command
        if err:
            jobid = None
        else:
            # debug dump 'out'
            debugmsg("sbatch output:\n------------\n{}------------\n".format(out))
            
            # extract job id from 'out'
            jobid = None
            for line in out.splitlines():
                match = re.match(r".*Submitted .* ([0-9]+).*$", line)
                if match:
                    jobid = match.group(1)
                    break
            if not jobid:
                err = "unexpected output from sbatch:\n{}".format(out)
                errormsg(err)
        
        return (jobid, out, err if err else 0)


    def _paramsFromConfiguration(self,):
        
        import configuration
    
        account   =  configuration.get("config.batch.params.account",   "commons")
        partition =  configuration.get("config.batch.params.partition", "commons")
        time      =  configuration.get("config.batch.params.time",      "1:00:00")
        
        return account, partition, time
        



# register this executor class by name
Executor.register("Slurm", SlurmExecutor)





