################################################################################
#                                                                              #
#  iterate.py                                                                  #
#  robustly iterates over build configs and test cases using a testdir         #
#      to store iteration state across failed partial iterations               #
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




class Iterate():

    
    @classmethod
    def doForAll(myClass, dims, args, numrepeats, study, wantBatch):
        
        from itertools import product
        from common import infomsg, errormsg, debugmsg, options
        from run import Run

        if not dims["tests"].paths():       # TODO: check every dimension for emptiness, not just 'tests' -- requires more structure in Spec classes
            infomsg("test spec matches no tests")
            return False
        else:
            
            debugmsg("experiment space = crossproduct( {} ) with args = {} and options = {} in study dir = {}"
                        .format(dims, args, options, study.path))

            if wantBatch:
            
                try:
                    
                    # TODO: optionally limit number of batch jobs in flight at once
                    
                    # schedule all tests for batch execution
                    infomsg("starting tests in batch")
                    submittedJobs = set()
                    for test, config, hpctoolkit, profile in product(dims["tests"], dims["build"], dims["hpctoolkit"], dims["profile"]):
                        jobID, errno = Run.submitJob(test.path(), config, hpctoolkit, profile, numrepeats, study)
                        if not errno:
                            submittedJobs.add(jobID)
                        else:
                            errormsg("submit failed for test at {}{}:{} ({})".format(test.path(), config, profile, err))
                        
                    # poll for finished jobs until all done
                    while submittedJobs:
                        finished = Run.pollForFinishedJobs()
                        submittedJobs.symmetric_difference_update(finished)  # since 'finished' containedIn 'submittedJobs', same as set subtract (not in Python)
                        for jobID in finished:
                            infomsg("test {} finished".format(Run.descriptionForJob(jobID)))
                        
                    infomsg("all tests finished")

                except Exception as e:
                    errormsg("batch failure: {}".format(e))
                
            else:
                
                # run all tests sequentially via shell commands
                for test, config, hpctoolkit, profile in product(dims["tests"], dims["build"], dims["hpctoolkit"], dims["profile"]):
                    run = Run(test.path(), config, hpctoolkit, profile, numrepeats, study, False)
                    status = run.run()
            
            




