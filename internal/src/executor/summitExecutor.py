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


class SummitExecutor(Executor):
    
 
    def __init__(self):
        
        super(SummitExecutor, self).__init__()
        # nothing for SummitExecutor
    
    # System inquiries

    @classmethod
    def isAvailable(cls):
        
        from common import whichDir
        import configuration
        
        available, msg = Executor._checkCmdsAvailable(["jsrun", "bsub", "bjobs"])
        available = available or configuration.get("batch.debug.force")
        
        return available, msg


    @classmethod
    def defaultToBackground(cls):
        
        return True

    
    # Programming model support
    
    def wrap(self, cmd, runPath, binPath, numRanks, numThreads, spackMPIBin):
        
        # TODO: USE binPath APPROPRIATELY!!!
        
        # spackMPIBin is unused
        # jsrun optiona per Summit User Guide (tinyurl.com/upx9fpm) and IBM documentation (tinyurl.com/re938v2)
        
        from os import getcwd
        import textwrap, tempfile
        from common import options, verbosemsg
                
        # get template
        template = \
            "jsrun {options} -i -n {numRanks} -a 1 -c {numThreads} {cmd}"   # could also say  -h {runPath}

        # insert parameters
        jsrunCmd = template.format(
            options      = "",          # or "--verbose" if "debug" in options else "", but jsrun apparently has no verbose option
            numRanks     = numRanks if numRanks > 0 else 1,
            numThreads   = numThreads if numThreads > 0 else 1,
            cmd          = cmd
            )
        
        return jsrunCmd

    
    # Scheduling operations
    
    def run(self, cmd, prelude, runPath, binPath, numRanks, numThreads, outPath, description): # returns nothing, raises
        
        # assumes that 'cmd' has been "wrapped" appropriately
        # 'prelude' is ignored
        
        from common import ExecuteFailed
        
        # run the specified command
        out, err = self._shell(cmd, binPath, runPath, outPath)
        
        if err: raise ExecuteFailed(out, err)

    
    def submitJob(self, cmd, numRanks, numThreads, name, description):   # returns jobID, out, err
        
        from common import ExecuteFailed

        jobid, out, err = self._bsub(cmd, numRanks, numThreads, name, description)
        if err == 0:
            self._addJob(jobid, description)
        
        return jobid, out, err

    
    def isFinished(self, jobID):
        
        return False    ## TODO: DEBUG

    
    def pollForFinishedJobs(self):
        
        import os, re
        from common import errormsg, fatalmsg
        
        # ask Summit for all our jobs that are still running
        out, err = self._shell("bjobs") # -UF == "don't format output", makes parsing easier

        # 'out' is a sequence of lines that look like this(see tinyurl.com/tttvygn):
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
            # match the job id, the first digit) sequence on the line
            match = re.match(r"([0-9]+) ", line)
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


    def _jsrun(self, cmd, runPath, binPath, numRanks, numThreads, outPath, description): # returns (out, err)
        
        from os import getcwd
        import textwrap, tempfile
        from common import options, verbosemsg
        
        # jsrun options per Summit User Guide (tinyurl.com/upx9fpm) and IBM documentation (tinyurl.com/re938v2)
        
        # slurm srun command template
        Summit_run_cmd_template = \
            "jsrun {options} -n 1 -a {numRanks} -c {numThreads} -h {runPath} {cmd}"
    
        # prepare summit command
        scommand = Summit_run_cmd_template.format(
            options      = "",          # jsrun apparently has no verbose option
            runPath      = runPath,
            numRanks     = numRanks,
            numThreads   = numThreads,
            cmd          = cmd
            )
        
        # run the command immediately with 'srun'
        verbosemsg("Executing via jsrun:\n{}".format(scommand))
        out, err = self._shell(scommand)
        
        return out, (err if err else 0)


    def _bsub(self, cmds, numRanks, numThreads, name, description): # returns (jobid, out, err)
        
        import textwrap, tempfile
        from os import getcwd
        from os.path import join
        import re
        import common
        from common import options, verbosemsg, debugmsg, errormsg
        
        # Summit sbatch command file template
        Summit_batch_file_template = textwrap.dedent(
            """\
            #!/bin/bash
            #BSUB -J {jobName}
            #BSUB -P {project}
            #BSUB -nnodes {numRanks}
            #BSUB -W {time}
            export OMP_NUM_THREADS={numThreads}
            {cmds} 
            """)
    
        # template params from configuration
        project, time = self._paramsFromConfiguration()
        
        # prepare Summit command file
        summitfilesDir = getcwd() if "debug" in options else join(common.homepath, ".hpctest")
        f = tempfile.NamedTemporaryFile(mode='w+t', bufsize=-1, delete=False,
                                        dir=summitfilesDir, prefix='summit-', suffix=".bsub")
        f.write(Summit_batch_file_template.format(
            jobName      = name,
            project      = project,
            numRanks     = numRanks,
            numThreads   = numThreads,
            time         = time,
            cmds         = cmds,
            ))
        f.close()
        
        # submit command file for batch execution with 'bsub'
        bsubOpts = ""    ## apparently bsub has no verbose option
        scommand = "bsub {} {}".format(bsubOpts, f.name)
        
        verbosemsg("submitting job {} ...".format(description))
        verbosemsg("    " + scommand)
        
        out, err = self._shell(scommand)
        
        verbosemsg("    " + out[:-1])   # don't print trailing newline
        
        # handle output from submit command
        # ... apparently looks like this (see tinyurl.com/wuh7rtg):
        # Job <29209> is submitted to default queue <batch>.
        
        # extract job id from 'out'
        if err:
            jobid = None
        else:
            # debug dump 'out'
            debugmsg("bsub output:\n------------\n{}\n------------\n".format(out))
            
            # extract job id from 'out'
            jobid = None
            for line in out.splitlines():
                match = re.match(r".*<([0-9]+)>.*", line)
                if match:
                    jobid = match.group(1)
                    break
            if not jobid:
                err = "unexpected output from bsub:\n{}".format(out)
                errormsg(err)
        
        return (jobid, out, err if err else 0)


    def _paramsFromConfiguration(self,):
        
        import configuration
        
        project = configuration.get("config.batch.params.project", "")
        time    = configuration.get("config.batch.params.time",    "0:05")
        
        return project, time
    



# register this executor class by name
Executor.register("Summit", SummitExecutor)





