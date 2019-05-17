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


class SlurmExecutor(Executor):
    
    
    def __init__(self):
        
        super(SlurmExecutor, self).__init__()
    

    @classmethod
    def defaultToBackground(cls):
        
        return True

    
    def run(self, cmd, runPath, env, numRanks, numThreads, outPath, description): # returns nothing, raises
        
        from common import ExecuteFailed
        rc, err = _srun(cmd, runPath, env, numRanks, numThreads, outPath, description)
        if rc:
            raise ExecuteFailed(err, "exit status {} ({})".format(rc, err))

    
    def submitJob(self, cmd, runPath, env, numRanks, numThreads, outPath, description):   # returns jobID, errno
        
        from common import ExecuteFailed

        jobid, rc, err = _sbatch(cmd, runPath, env, numRanks, numThreads, outPath, description)
        if rc == 0:
            self.runningProcesses.add(jobid)
            self.jobDescriptions[jobid] = description
        
        return (jobid, err)      

    
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




def _shell(cls, cmd):
           
    import subprocess
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    return (out, err)


def _srun(cmd, runPath, env, numRanks, numThreads, outPath, description): # returns (rc, err)
    
    import textwrap, tempfile
    
    # slurm srun command file template
    #   args: jobName, account, partition, nnodes, ntasks, time, outpath, errorpth, cmd
    _Slurm_run_template = textwrap.dedent(
        """\
        #!/bin/bash
        #SBATCH --job-name={jobName}
        #SBATCH --account={account}
        #SBATCH --partition={partition}
        #SBATCH --export={env}
        #SBATCH --nodes={nnodes}
        #SBATCH --exclusive
        #SBATCH --ntasks={ntasks}
        #### #SBATCH --ntasks-per-node=4
        #SBATCH --cpus-per-task={cpusPerTask}    # 2
        #SBATCH --mem-per-cpu={memPerCpu}        # 1000m
        #SBATCH --time={time}
        #SBATCH --output={outPath}
        #SBATCH --error={errorPath}
        #SBATCH --mail-type=NONE
        {cmd}
        """)

    # template params from configuration
    account, partition, time = _paramsFromConfiguration()

    # template params from test
    cpusPerTask, memPerCpu = _paramsFromTest()
    
    # prepare slurm command file
    f, fname = tempfile.mkstemp(".slurm")
    f.write(_Slurm_run_template.format(
        jobName     = description,
        account     = account,
        partition   = partition,
        env         = _envDictToString(env),
        nnodes      = numRanks,
        ntasks      = numThreads,
        cpusPerTask = cpusPerTask,      # 2,
        memPerCpu   = memPerCpu,        # "1000m",
        time        = time,
        outPath     = outPath,
        errorPath   = outPath + ".err",
        cmd         = cmd,
        ))
    f.close()
    
    # run the command immediately with 'srun'
    out, err = _shell("srun {}".format(fname))
    # extract rc from 'out'
    rc = 0
    
    return (rc, err)


def _sbatch(cmd, runPath, env, numRanks, numThreads, outPath, description): # returns (jobid, rc, err)
    
    import textwrap, tempfile
    from os import getcwd
    
    # slurm sbatch command file template
    #   args: jobName, account, partition, nnodes, ntasks, time, outpath, errorpth, cmd
    _Slurm_batch_template = textwrap.dedent(
        """\
        #!/bin/bash
        #SBATCH --job-name={jobName}
        #SBATCH --account={account}
        #SBATCH --partition={partition}
        #SBATCH --export={env}
        #SBATCH --nodes={nnodes}
        #SBATCH --exclusive
        #SBATCH --ntasks={ntasks}
        #SBATCH --cpus-per-task={cpusPerTask}    # 2
        #SBATCH --mem-per-cpu={memPerCpu}        # 1000m
        #SBATCH --time={time}
        #SBATCH --output={outPath}
        #SBATCH --error={errorPath}
        #SBATCH --mail-type=NONE
        {cmd} 
        """)

    # template params from configuration
    account, partition, time = _paramsFromConfiguration()
    
    # template params from test
    cpusPerTask, memPerCpu = _paramsFromTest()
    
    # prepare slurm command file
    f = tempfile.NamedTemporaryFile(mode='w+t', bufsize=-1, suffix=".slurm", prefix='tmp', dir=getcwd(), delete=False)
    f.write(_Slurm_batch_template.format(
        jobName     = description,
        account     = account,
        partition   = partition,
        env         = _envDictToString(env),
        nnodes      = numRanks,
        ntasks      = numThreads,
        cpusPerTask = cpusPerTask,      # 2,
        memPerCpu   = memPerCpu,        # "1000m",
        time        = time,
        outPath     = outPath + ".out" if outPath else "slurm-%x.out",
        errorPath   = outPath + ".err" if outPath else "slurm-%x.err",
        cmd         = cmd
        ))
    f.close()
    
    # submit the command for batch execution with 'sbatch'
    out, err = _shell("sbatch {}".format(fname))
    # extract job id from 'out'
    jobid = 17
    # extract rc from 'out'
    rc = 0
    
    return (jobid, rc, err)


def _envDictToString(envDict):
    
    s = ""
    for key, value in envDict.iteritems():
        s += (key + "=" + value + " ")
    return s


def _paramsFromConfiguration():
    
    import configuration
##      account   =  configuration.get(xxx, "xxx")
##        partition =  configuration.get(xxx, "xxx")
##        time      =  configuration.get(xxx, "xxx")
    account   =  "scott@rice.edu"
    partition =  "common"
    time      =  "0:30:00"
    
    return (account, partition, time)


def _paramsFromTest():
    
    import configuration

    cpusPerTask = 1
    memPerCpu   = "1000m"
    
    return (cpusPerTask, memPerCpu)




# register this executor class by name
Executor.register("Slurm", SlurmExecutor)





